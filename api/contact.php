<?php
/**
 * Main Street - contact / newsletter form handler.
 *
 * - Accepts POST from the site forms (fields: Name, E-mail, Phone, Message).
 * - Silently rejects bots (honeypot fields + minimum fill time is not used, keeps it simple).
 * - Always stores the submission in api/data/submissions.jsonl (not web-accessible, see .htaccess).
 * - Also e-mails the team when a recipient is set in api/config.php (CONTACT_TO).
 */
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

function out($code, $arr) { http_response_code($code); echo json_encode($arr); exit; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') out(405, ['ok' => false, 'error' => 'Method not allowed.']);

$cfg = ['CONTACT_TO' => '', 'CONTACT_FROM' => 'no-reply@mainstreet.landingprofile.com'];
if (is_file(__DIR__ . '/config.php')) { $c = include __DIR__ . '/config.php'; if (is_array($c)) $cfg = array_merge($cfg, $c); }

// Honeypots: real visitors never fill these hidden fields.
foreach (['website','company','message','comments','description','details','feedback','notes','remarks','subject','title'] as $h) {
    if (isset($_POST[$h]) && trim((string)$_POST[$h]) !== '') out(200, ['ok' => true]); // pretend success to bots
}

function clean($v, $max) {
    $v = trim((string)$v);
    $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/', '', $v);
    return mb_substr($v, 0, $max);
}

$name    = clean($_POST['Name'] ?? '', 120);
$email   = clean($_POST['E-mail'] ?? ($_POST['Email'] ?? ''), 160);
$phone   = clean($_POST['Phone'] ?? '', 40);
$message = clean($_POST['Message'] ?? '', 4000);
$page    = clean($_POST['page'] ?? '', 200);

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) out(422, ['ok' => false, 'error' => 'Please enter a valid email address.']);
$isContact = ($name !== '' || $message !== '');
if ($isContact && $name === '') out(422, ['ok' => false, 'error' => 'Please enter your name.']);

// very small rate limit: 1 submission per 10 seconds per IP
$ip = $_SERVER['REMOTE_ADDR'] ?? '';
$dir = __DIR__ . '/data';
if (!is_dir($dir)) { @mkdir($dir, 0750, true); }
$stamp = $dir . '/rl_' . md5($ip);
if (is_file($stamp) && (time() - filemtime($stamp)) < 10) out(429, ['ok' => false, 'error' => 'Please wait a few seconds before sending again.']);
@touch($stamp);

$row = [
    'time'    => gmdate('c'),
    'type'    => $isContact ? 'contact' : 'newsletter',
    'name'    => $name, 'email' => $email, 'phone' => $phone, 'message' => $message,
    'page'    => $page, 'ip' => $ip,
];
$saved = @file_put_contents($dir . '/submissions.jsonl', json_encode($row, JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX) !== false;

$mailed = false;
if ($cfg['CONTACT_TO'] !== '') {
    $subject = ($isContact ? 'New Main Street inquiry from ' . $name : 'New Main Street newsletter sign-up');
    $subject = preg_replace('/[\r\n]+/', ' ', $subject);
    $body = "Type: {$row['type']}\nName: $name\nEmail: $email\nPhone: $phone\nPage: $page\n\nMessage:\n$message\n";
    $headers = "From: Main Street <{$cfg['CONTACT_FROM']}>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=utf-8";
    $mailed = @mail($cfg['CONTACT_TO'], $subject, $body, $headers);
}

if ($saved || $mailed) out(200, ['ok' => true]);
out(500, ['ok' => false, 'error' => 'We could not send your message right now. Please try again later.']);
