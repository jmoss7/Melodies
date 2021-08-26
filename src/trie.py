class TrieNode:
    def __init__(self, val: str, parent, rating: int = -1):
        """ A TrieNode is a node within the MelodyTrie object implemented
            below """

        if not isinstance(parent, TrieNode):
            parent = None

        self.val: str = val  # The name of the note (sharps and regular only)

        # The rating of the melody up to (and including) this node
        self.rating: int = rating

        # The average of the melodies that include this node
        self.cumulativeRating: int = rating

        self.parent: TrieNode = parent  # Node that this node is a child of

        # The nodes of subsequent notes in melodies this note is a part of
        self.children: dict[str, TrieNode] = {}


class MelodyTrie:
    def __init__(self):
        """ A MelodyTrie is an object used to represent all of the melodies
            saved in a taste.mel by utilizing the Trie data structure. """

        self.root = TrieNode("Root", None)

    def __repr__(self):
        return str(self)

    def __str__(self):
        level = 0
        res = f"0: Root(CR={self.root.cumulativeRating})"
        nextLevel = list(self.root.children.values())

        while nextLevel:
            level += 1
            res += f"\n{level}: "
            levelSize = len(nextLevel)
            for i in range(levelSize):
                res += (f"{nextLevel[0].val}(R={nextLevel[0].rating}" +
                        f",CR={nextLevel[0].cumulativeRating}) ")
                if i < levelSize - 1:
                    res += "| "
                nextLevel += list(nextLevel[0].children.values())
                nextLevel.pop(0)

        return res


    def isEmpty(self):
        """ Whether a melody has been added to the trie or not """

        return len(self.root.children) == 0

    def addMelody(self, noteList: list[str], rating: int):
        """ Adds a melody to the trie and updates cumulative ratings along
            the search (only adds new nodes if it does not exist already """

        if not noteList:
            return

        curNode = self.root

        for n in noteList:
            curNode.cumulativeRating += rating
            curNode.cumulativeRating = curNode.cumulativeRating // 2
            if not curNode.children.get(n, False):
                curNode.children[n] = TrieNode(n, curNode)

            curNode = curNode.children.get(n)

        if curNode.rating == -1:
            curNode.cumulativeRating = rating
        else:
            curNode.cumulativeRating += rating
            curNode.cumulativeRating = curNode.cumulativeRating // 2

        if curNode.val != "Root":
            curNode.rating = rating

    def getRating(self, noteList: list[str]):
        """ Given the notes of a melody in note form, returns the rating of
            the melody using the trie as a reference """

        curNode = self.root
        endOfMelody = True  # Whether the entire melody was found in trie

        for n in noteList:
            if curNode.children.get(n, False):
                curNode = curNode.children.get(n)
            else:
                endOfMelody = False
                break

        if endOfMelody and curNode.val != "Root":
            return curNode.rating

        return curNode.cumulativeRating

    def traverse(self, start: TrieNode, path: list[str],
                 backwards: bool = False):
        """ Given a starting position (node), either move down (forward) the
            trie or up the trie (backwards) following the given path of notes.
            Returns the node that appears at the end of the path """

        curNode = start
