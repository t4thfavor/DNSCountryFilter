import json
import urllib3
import pprint
import struct

class iplocator:
    countrylist = []

    def __init__(self):
        global countrylist
        countrylist = self.LoadList()

    def LoadList(self):
        text_file = open("/home/chance/countries.dat", "r")
        list = text_file.read().splitlines()
        return list

    def IsBlockedIP(self,addr):
        #countrylist = self.LoadList()
        http = urllib3.PoolManager()
        url = 'http://ipinfo.io/'+str(addr)+'/json'
        resp = http.request("GET",url)
        #s = ur.urlopen(url)
        #sl = s.read()
        data = json.loads(resp.data) #json.load(resp.json())

        #IP=data['ip']
        #org=data['org']
        #city = data['city']
        country=data['country']
        #region=data['region']
        print("IP from country %s", country)
        if country in countrylist:
            return True
        
        return False


class dnslib333:

    DNS_QUERY_SECTION_FORMAT = struct.Struct("!2H")
    DNS_QUERY_MESSAGE_HEADER = struct.Struct("!6H")

    def decode_labels(self,message, offset):
        labels = []

        while True:
            length, = struct.unpack_from("!B", message, offset)

            if (length & 0xC0) == 0xC0:
                pointer, = struct.unpack_from("!H", message, offset)
                offset += 2

                return labels + self.decode_labels(message, pointer & 0x3FFF), offset

            if (length & 0xC0) != 0x00:
                raise StandardError("unknown label encoding")

            offset += 1

            if length == 0:
                return labels, offset

            labels.append(*struct.unpack_from("!%ds" % length, message, offset))
            offset += length


    def decode_question_section(self,message, offset, qdcount):
        questions = []

        for _ in range(qdcount):
            qname, offset = self.decode_labels(message, offset)

            qtype, qclass = self.DNS_QUERY_SECTION_FORMAT.unpack_from(message, offset)
            offset += self.DNS_QUERY_SECTION_FORMAT.size

            question = {"domain_name": qname,
                        "query_type": qtype,
                        "query_class": qclass}

            questions.append(question)

        return questions, offset
    

    def decode_dns_message(self,message):

        id, misc, qdcount, ancount, nscount, arcount = self.DNS_QUERY_MESSAGE_HEADER.unpack_from(message)

        qr = (misc & 0x8000) != 0
        opcode = (misc & 0x7800) >> 11
        aa = (misc & 0x0400) != 0
        tc = (misc & 0x200) != 0
        rd = (misc & 0x100) != 0
        ra = (misc & 0x80) != 0
        z = (misc & 0x70) >> 4
        rcode = misc & 0xF

        offset = self.DNS_QUERY_MESSAGE_HEADER.size
        questions, offset = self.decode_question_section(message, offset, qdcount)

        result = {"id": id,
                "is_response": qr,
                "opcode": opcode,
                "is_authoritative": aa,
                "is_truncated": tc,
                "recursion_desired": rd,
                "recursion_available": ra,
                "reserved": z,
                "response_code": rcode,
                "question_count": qdcount,
                "answer_count": ancount,
                "authority_count": nscount,
                "additional_count": arcount,
                "questions": questions}

        return result