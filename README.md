# hashdb-api
## client
Not only can blocks be collected from files, images and memory but it also can be carved from packet captures using the Bro script.
```
bro -r 2015-07-20-Nuclear-EK-sends-TeslaCrypt-2.0-traffic.pcap fileblocks.bro | sort | uniq > pcap_blocks_out.txt
```
The example client code removes duplicates from the text file to limit the number of necessary network calls to the API before producing the results written to a text file.
```
hashdb-api.py -f pcap_blocks_out.txt > block_analysis_out.txt
```
Review the output looking for block hashes that appear in one or more samples based on count from the VirusShare.com collection.  Additional information is available on which samples contained the matching blocks by referencing the FileBlock.Info project.
## server
The hashdb-api server requires that Twisted Python and HashDB be installed with the appropriate permissions prior to starting the TCP socket.
```
twistd -y hashdb.tac
```
