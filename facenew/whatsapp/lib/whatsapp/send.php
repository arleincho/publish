<?php
set_time_limit(10);
require_once 'whatsprot.class.php';
require_once 'contacts.php';

$debug = true;

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
$image  = $argv[5];

$id = $argv[6];

function onMessageReceivedServer($phone, $from, $id, $type, $t){
	$conn_string = "host=localhost port=5432 dbname=alquiler_perfil user=Dj4ngoU53rD4t4b4s3 password=Fvnja32QpxEZ5ppJYPmfP8umKKJGT2wH";
	$db = pg_connect('alquiler_perfil=foo');
	$data = array('id' => 2);
	$res = pg_update($db, 'whatsapp_messagesphonewhatsapp', array('message_whatsapp_id' => $id, 'sended_at' => date("Y-m-d H:i:s")), $data);
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
