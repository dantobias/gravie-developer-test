<?php
header("Content-Type: text/html; charset=utf-8");

$ch = curl_init();
#curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
#curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0');
curl_setopt($ch, CURLOPT_REFERER, 'https://gtest.dan.info/');
$url = 'http://www.giantbomb.com/api/game/3030-4725/?api_key=9f5f504612747bac723f6776a7e63514959350e2&format=json';
curl_setopt($ch, CURLOPT_URL, $url);
$result = curl_exec($ch);
curl_close($ch);

#$obj = json_decode($result);
?>
<!doctype html>
<html lang="en-us">
<head>
  <meta charset="utf-8">
  <meta name="description" content="A test web app">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Test</title>
</head>
<body>
    <h1>Hello World</h1>
    <pre><?php echo '"'.$result.'"'; ?></pre>
</body>