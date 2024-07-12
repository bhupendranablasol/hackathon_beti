<?php
// error_reporting(0);

header('Access-Control-Allow-Origin: *');

header('Access-Control-Allow-Methods: GET, POST');

header("Access-Control-Allow-Headers: X-Requested-With");

use Slim\Factory\AppFactory;
use Slim\Factory\ServerRequestCreatorFactory;


require __DIR__ . '/vendor/autoload.php';
include __DIR__ . '/functions.php';

$app = AppFactory::create();

$app->post('/extract', function ($request, $response, $args) {
  $parsedBody = $request->getParsedBody();
  $entities = $parsedBody['entities'];
  $uploadedFiles = $request->getUploadedFiles();
  $document = $uploadedFiles['file'];
  $filePath = $document->getStream()->getMetadata('uri');

  $text = extractTextFromPdf($filePath);
  $data = extractStructuredData($text, $entities);
  $response->getBody()->write($data);
  return $response->withHeader('Content-Type', 'application/json');
});

try {
  $app->run();
} catch (Exception $e) {
  // We display a error message
  die(json_encode(array("status" => "failed", "message" => "This action is not allowed")));
}
