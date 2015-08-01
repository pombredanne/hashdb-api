# This file is part of Viper - https://github.com/botherder/viper
# See the file 'LICENSE' for copying permission.

import os
import json

from viper.common.out import cyan
from viper.common.utils import hexdump
from viper.common.abstracts import Module
from viper.core.session import __sessions__

try:
    import bulk_extractor
    HAVE_BULK_EXTRACTOR = True
except ImportError:
    HAVE_BULK_EXTRACTOR = False

class BulkExtractor(Module):
    cmd = 'bulk_extractor'
    description = 'Parse binaries with bulk_extractor'
    authors = ['John B. Lukach']

    def __init__(self): 
        super(BulkExtractor, self).__init__()
        self.parser.add_argument('-s','--scan',action='store_true',help='Scan file with bulk_extractor')
        self.parser.add_argument('-e','--email',action='store_true',help='List email addresses found')
        self.parser.add_argument('-i','--ip',action='store_true',help='List ip addresses found')
        self.parser.add_argument('-d','--domain',action='store_true',help='List domain addresses found')
        self.parser.add_argument('-b','--blocks',action='store_true',help='List matching blocks found')
        self.parser.add_argument('-v','--view',action='store_true',help='Display hex view of blocks')
        self.parser.add_argument('-l','--list',action='store_true',help='Samples with matching blocks')

    def scan(self):        
        if os.path.exists(__sessions__.current.file.path+'_dir'):
            self.log('info',"The bulk_extractor scan has already completed")
        else: 
            if os.path.exists('FileBlock.Info'): 
                self.log('info',"Running bulk_extractor with hashdb enabled")     
                os.system('bulk_extractor -e hashdb -S hashdb_mode=scan -S hashdb_scan_path_or_socket=FileBlock.Info -o '+__sessions__.current.file.path+'_dir '+__sessions__.current.file.path)
            else:
                self.log('warning',"Running bulk_extractor, maybe download the FileBlock.Info hashdb")
                self.log('info',"https://github.com/jblukach/FileBlock.Info")
                os.system('bulk_extractor -o '+__sessions__.current.file.path+'_dir '+__sessions__.current.file.path)

    def email(self):            
        if os.path.isfile(__sessions__.current.file.path+'_dir/email_histogram.txt'):
            file = open(__sessions__.current.file.path+'_dir/email_histogram.txt','r')
            file.readline()
            file.readline()
            file.readline()
            file.readline()
            file.readline()
            for line in file:  
                self.log('item',line)
            file.close()
        else:
            self.log('warning',"Must -s or --scan with bulk_extractor first")

    def ip(self):    
        if os.path.isfile(__sessions__.current.file.path+'_dir/ip_histogram.txt'):
            file = open(__sessions__.current.file.path+'_dir/ip_histogram.txt','r')
            file.readline()
            file.readline()
            file.readline()
            file.readline()
            file.readline()
            for line in file:
                self.log('item',line)
            file.close()
        else:
            self.log('warning',"Must -s or --scan with bulk_extractor first")

    def domain(self):    
        if os.path.isfile(__sessions__.current.file.path+'_dir/domain_histogram.txt'):
            file = open(__sessions__.current.file.path+'_dir/domain_histogram.txt','r')
            file.readline()
            file.readline()
            file.readline()
            file.readline()
            file.readline()
            for line in file:
                self.log('item',line)
            file.close()
        else:
            self.log('warning',"Must -s or --scan with bulk_extractor first")

    def blocks(self):    
        if os.path.isfile(__sessions__.current.file.path+'_dir/identified_blocks.txt'):
            file = open(__sessions__.current.file.path+'_dir/identified_blocks.txt','r')
            file.readline()
            file.readline()
            file.readline()
            file.readline()
            file.readline()
            for line in file:
                self.log('item',line)
            file.close()
        else:
            self.log('warning',"Must -s or --scan with bulk_extractor with hashdb enabled first")
            self.log('info',"https://github.com/simsong/hashdb")

    def view(self):    
        offset_input = input("Enter numeric offset: ")
        self.log('',offset_input)
        self.log('', cyan(hexdump(__sessions__.current.file.data[offset_input:], maxlines=32)))
        self.log('',offset_input+512)
        self.log('', cyan(hexdump(__sessions__.current.file.data[offset_input+512:], maxlines=32)))
        self.log('',offset_input+1024)
        self.log('', cyan(hexdump(__sessions__.current.file.data[offset_input+1024:], maxlines=32)))
        self.log('',offset_input+1536)
        self.log('', cyan(hexdump(__sessions__.current.file.data[offset_input+1536:], maxlines=32)))
        self.log('',offset_input+2048)
        self.log('', cyan(hexdump(__sessions__.current.file.data[offset_input+2048:], maxlines=32)))
        self.log('',offset_input+2560)
        self.log('', cyan(hexdump(__sessions__.current.file.data[offset_input+2560:], maxlines=32)))
        self.log('',offset_input+3072)
        self.log('', cyan(hexdump(__sessions__.current.file.data[offset_input+3072:], maxlines=32)))
        self.log('',offset_input+3584)
        self.log('', cyan(hexdump(__sessions__.current.file.data[offset_input+3584:], maxlines=32)))
        self.log('',offset_input+4096)

    def list(self):
        hash_input = raw_input("Enter block hash: ")
        if os.path.exists('FileBlock.Info'): 
            os.system('hashdb scan_expanded_hash FileBlock.Info '+hash_input+' > '+__sessions__.current.file.path+'_dir/'+hash_input+'.json')
            file = open(__sessions__.current.file.path+'_dir/'+hash_input+'.json','r')
            file.readline()
            file.readline()
            file.readline() 
            data = file.readline()
            try: 
                j = json.loads(data) 
                parent =  j["sources"]
                for item in parent:
                    self.log('item',item["filename"])
            except: 
                self.log('item','Exceeded the default number of hashes printed by hashdb') 
            file.close()
        else:
            self.log('warning',"Download the FileBlock.Info hashdb to search")
            self.log('info',"https://github.com/jblukach/FileBlock.Info")

    def usage(self):
        self.log('',"Usage: bulk_extractor -s --scan|-e --email|-i --ip|-d --domain|-b --blocks|-v --view|-l --list")

    def run(self):
        super(BulkExtractor, self).run()
        if self.args is None:
            return
       
        if not HAVE_BULK_EXTRACTOR:
            self.log('error',"Missing dependency, install bulk_extractor with hashdb")
            self.log('info',"https://github.com/simsong/bulk_extractor")

        if not __sessions__.is_set():
            self.log('error',"No session opened")
       
        if __sessions__.is_set(): 
            if self.args.scan:
                self.scan()
            elif self.args.email:
                self.email()
            elif self.args.ip:
                self.ip()
            elif self.args.domain:
                self.domain()
            elif self.args.blocks:
                self.blocks()
            elif self.args.view:
                self.view()
            elif self.args.list:
                self.list()
            else:
                self.log('error','At least one of the parameters is required')
                self.usage()
