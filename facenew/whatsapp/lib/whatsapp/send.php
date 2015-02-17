<?php
set_time_limit(10);
require_once 'whatsprot.class.php';
require_once 'contacts.php';

$debug = true;

$username = "573133271344";
$identity = "355849055773122";
$password = "VLkes03pzaAIehEc0cNdeCj2eXM=";
// $target = "573003250046";
$target = "573123188228";
$message = "Hola";
$image = "http://arley.co/unnamed.png";

$nickname = "Arley";

// $username = $argv[1];
// $identity = $argv[2];
// $password = $argv[3];
// $target   = $argv[4];
// $message  = $argv[5];
// $image  = $argv[7];

$id = $argv[6];

function onMessageReceivedServer($phone, $from, $message_id, $type, $t){
	global $id;
	print "sdfsadfsdf";
	// $conn_string = "host=localhost port=5432 dbname=alquiler_perfil user=Dj4ngoU53rD4t4b4s3 password=Fvnja32QpxEZ5ppJYPmfP8umKKJGT2wH";
	// $db = pg_connect($conn_string);
	// $data = array('id' => $id);
	// $res = pg_update($db, 'whatsapp_messagesphonewhatsapp', array('message_whatsapp_id' => $message_id, 'sended_at' => date("Y-m-d H:i:s"), 'sended' => true), $data);
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
