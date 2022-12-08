String data = new File('resources/day6.txt').getText()

int START_OF_PACKET_MARKER_SIZE = 4
int START_OF_PACKET_MESSAGE_SIZE = 14

static def checkUnique(Queue<Character> chars) {
    return new HashSet<>(chars).size() == chars.size();
}

def static findMarketIndex(String data, int uniqueCharacterCount) {
    Queue<Character> packet = data.substring(0, uniqueCharacterCount).chars as LinkedList

    for (int i = uniqueCharacterCount; i < data.length(); i++) {
        if (checkUnique(packet)) {
            return i
        }
        packet.remove()
        packet.add(data[i] as char)
    }
}

print("Start of packet marker found " + findMarketIndex(data, START_OF_PACKET_MARKER_SIZE) + "\n")
print("Start of message marker found " + findMarketIndex(data, START_OF_PACKET_MESSAGE_SIZE))



