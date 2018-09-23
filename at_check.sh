#cat /dev/smd7  >> /bin/at_result.txt &

echo -e "at+gsn\r\n" > /dev/smd7
echo -e "at+csim=10,\"00B0090910\"\r\n" > /dev/smd7
