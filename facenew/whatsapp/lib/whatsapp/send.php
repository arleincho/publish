<?php
set_time_limit(10);
require_once 'whatsprot.class.php';
require_once 'contacts.php';

$debug = false;

// $username = "573123846473";
// $identity = "356971040682553";
// $password = "EtAQwdXHzN6GFvhojzACvrWuj4s=";
// $target = "573203425072";

$nickname = "Angela Robledo";

$username = $argv[1];
$identity = $argv[2];
$password = $argv[3];
$target   = $argv[4];
$message  = $argv[5];
$image  = $argv[7];

$id = $argv[6];

function onMessageReceivedServer($phone, $from, $message_id, $type, $t){
	global $id;
	$conn_string = "host=localhost port=5432 dbname=alquiler_perfil user=Dj4ngoU53rD4t4b4s3 password=Fvnja32QpxEZ5ppJYPmfP8umKKJGT2wH";
	$db = pg_connect($conn_string);
	$data = array('id' => $id);
	$res = pg_update($db, 'whatsapp_messagesphonewhatsapp', array('message_whatsapp_id' => $message_id, 'sended_at' => date("Y-m-d H:i:s"), 'sended' => true), $data);
}

$w = new WhatsProt($username, $identity, $nickname, $debug);
$w->connect();

$w->loginWithPassword($password);
$w->eventManager()->bind("onMessageReceivedServer", "onMessageReceivedServer");
$w->sendMessage($target, $message);
if ($image){
	$w->sendMessageImage($target, $image);
}
$w->pollMessages();
