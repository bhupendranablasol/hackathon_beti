<?php

require __DIR__ . '/vendor/autoload.php';

use Smalot\PdfParser\Parser;

function extractTextFromPdf($filePath)
{
    $parser = new Parser();
    $pdf = $parser->parseFile($filePath);
    $text = $pdf->getText();
    return cleanText($text);
}

function cleanText($text)
{
    // $text = strtolower($text);
    // $text = preg_replace('/[^a-z0-9\s]/', '', $text);
    // $text = trim($text);
    return $text;
}

function extractStructuredData($text, $entities)
{
    // Regular expressions
    $emailPattern = '/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/';
    $ssnPattern = '/\b\d{3}-\d{2}-\d{4}\b/';
    $phonePattern = '/\b\d{10}\b/';
    $emails = array();
    $ssns = array();
    $phones = array();

    preg_match_all($emailPattern, $text, $emails);
    preg_match_all($phonePattern, $text, $phones);
    preg_match_all($ssnPattern, $text, $ssns);

    // Call Python script for NER (assumed to be trained and ready)
    $tempFile = tempnam(sys_get_temp_dir(), 'document');
    $myfile = fopen("testData.txt", "w") or die("Unable to open file!");

    fwrite($myfile, $text);
    file_put_contents($tempFile, $text);


    // Define the command to execute the Python script
    $command = "python ../modeltrainer/document.py ../apis/testData.txt $entities";
    $output = shell_exec($command);
    $result = json_decode($output, true);
    $result['emails'] = $emails[0];
    $result['phones'] = $phones[0];
    $result['ssns'] = $ssns[0];

    return json_encode($result);
}
