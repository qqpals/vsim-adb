sync

cat /dev/smd7 & echo -e "at+qcfg=\"sim/softsimmode\",2\r\n" > /dev/smd7

cat /dev/smd7 & echo -e "at+qprtpara=1 \r\n" > /dev/smd7

sys_reboot

