<?php

$temp_dir = str_replace('\\', '\\\\', $template_directory);
$work_dir = str_replace('\\', '\\\\', $working_directory);

// Define the path to the 'run_opensim_example.bat' batch file in the template directory
$batch_file_path = $temp_dir . DIRECTORY_SEPARATOR . 'run_opensim_example.bat';

// Prepare the command to run the batch file, now passing the working directory path as an argument
$command = 'cd "' . escapeshellarg($temp_dir) . '" && cmd /c "' . escapeshellarg($batch_file_path) . ' ' . escapeshellarg($work_dir) . '"';

// Execute the command within a new Command Prompt window
exec($command);

echo "Batch file 'run_opensim_example.bat' has been executed and the working directory has been opened.";
?>
