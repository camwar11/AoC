from typing import Tuple
import math

from common.utilityfunctions import hex2bin_leading_zeros, split_seq


class BITSPacket(object):
    versionSize = 3
    typeIDSize = 3
    headerSize = versionSize + typeIDSize

    literalSize = 5
    lengthTypeIdSize = 1
    lengthSize = 15
    numSubPacketSize = 11

    TYPE_ID_LITERAL = 4
    LENGTH_TYPE_ID_TOTAL_LENGTH = 0
    LENGTH_TYPE_ID_TOTAL_NUM_SUB_PACKETS = 1

    

    def __init__(self) -> None:
        super().__init__()
        
        self.decodedData = None
        self.version = None
        self.typeId = None
        self.subPackets = []
        self.type_id_functions = {
            0: self.__sum,
            1: self.__product,
            2: self.__minimum,
            3: self.__maximum,
            5: self.__greater_than,
            6: self.__less_than,
            7: self.__equal_to,
        }

    def __sum(self):
        return sum([x.decodedData for x in self.subPackets])

    def __product(self):
        return math.prod([x.decodedData for x in self.subPackets])

    def __minimum(self):
        return min([x.decodedData for x in self.subPackets])

    def __maximum(self):
        return max([x.decodedData for x in self.subPackets])

    def __greater_than(self):
        if self.subPackets[0].decodedData > self.subPackets[1].decodedData:
            return 1
        return 0

    def __less_than(self):
        if self.subPackets[0].decodedData < self.subPackets[1].decodedData:
            return 1
        return 0

    def __equal_to(self):
        if self.subPackets[0].decodedData == self.subPackets[1].decodedData:
            return 1
        return 0

    
    @staticmethod
    def parse(message: str, isHex: bool = False):
        packet = BITSPacket()
        if isHex:
            message = hex2bin_leading_zeros(message)

        header, data = split_seq(message, BITSPacket.headerSize)
        leftoverData = data

        packet.version, header = BITSPacket.__split_and_parse_bin(header, BITSPacket.versionSize)
        packet.typeId, header = BITSPacket.__split_and_parse_bin(header, BITSPacket.typeIDSize)

        packet.decodedData = ''
        if packet.typeId == BITSPacket.TYPE_ID_LITERAL:
            packet.decodedData, leftoverData = BITSPacket.__parseLiterals(data)
        else:
            lengthTypeId, data = BITSPacket.__split_and_parse_bin(data, BITSPacket.lengthTypeIdSize)
            if lengthTypeId == BITSPacket.LENGTH_TYPE_ID_TOTAL_LENGTH:
                length, data = BITSPacket.__split_and_parse_bin(data, BITSPacket.lengthSize)
                data, leftoverData = split_seq(data, length)
                while data and len(data) > 0:
                    subPacket, data = BITSPacket.parse(data)
                    packet.subPackets.append(subPacket)
            else:
                numSubPackets, data = BITSPacket.__split_and_parse_bin(data, BITSPacket.numSubPacketSize)
                for i in range(numSubPackets):
                    subPacket, data = BITSPacket.parse(data)
                    packet.subPackets.append(subPacket)
                leftoverData = data
            
            packet.decodedData = packet.type_id_functions[packet.typeId]()
        
        return packet, leftoverData

    @staticmethod
    def __split_and_parse_bin(data:str, length: int) -> Tuple[int, str]:
        rawBin, remainder = split_seq(data, length)
        return int(rawBin, 2), remainder
        
    @staticmethod
    def __parseLiterals(data: str):
        decodedData = ''
        while(True):
            if len(data) < BITSPacket.literalSize:
                return int(decodedData, 2), ''
            literal = data[:BITSPacket.literalSize]
            literalPrefix = literal[0]
            literalValue = literal[1:]
            decodedData += str(literalValue)
            data = data[BITSPacket.literalSize:]
            if literalPrefix == '0':
                return int(decodedData, 2), data
