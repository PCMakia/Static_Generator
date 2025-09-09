from textnode import TextType,TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
        list_word = node.text.split()
        indexes = find_match(list_word,delimiter,text_type)
        if isinstance(indexes, list):
            res.append(TextNode(" ".join(list_word[0:indexes[0]]), node.text_type))
            res.append(TextNode(" ".join(list_word[indexes[0]:indexes[1]+1]), text_type))
            res.append(TextNode(" ".join(list_word[indexes[1]+1:]), node.text_type))
        else:
            res.append(indexes)
    return res


# find matching closing delimiter, return index if found and false if not found
def find_match(list_word,delimiter,text_type):
    found = 0
    there = False
    start_end = []
    for i in range(len(list_word)):
        if list_word[i][0] == delimiter and list_word[i][-1] == delimiter:
            return TextNode(list_word[i],text_type)
        if list_word[i][0] == delimiter:
            found += 1
            start_end.append(i)
        if list_word[i][-1] == delimiter and found == 1:
            found -= 1
            start_end.append(i)
            return start_end


        if found > 1: 
            raise Exception("Nested element is not allowed, for now") 
    raise Exception("No closing delimeter found")
