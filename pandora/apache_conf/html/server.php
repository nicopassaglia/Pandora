<?php

$key = $_POST['key'];


$url = 'http://127.0.0.1:5000/post_key?key='.$key;

$contents = file_get_contents($url);

echo $contents;

?>
