# hashdb-api
## client

```
bro -r 2015-07-20-Nuclear-EK-sends-TeslaCrypt-2.0-traffic.pcap fileblocks.bro | sort | uniq > pcap_blocks_out.txt
```

```
hashdb-api.py -f pcap_blocks_out.txt
```

## server

```
twistd -y hashdb.tac
```
