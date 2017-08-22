from ply import *
import dlib

def ply_parse(text):

    keywords = {"true": "TRUE", "false": "FALSE"}
    
    tokens = (["SYMBOL","COMMA", "PO", "PC", "NOT", "AND", "OR", "IMPLIES"] +
              list(keywords.values()))

    def t_SYMBOL(t):
        r"[a-zA-Z]\w*"
        t.type = keywords.get(t.value, "SYMBOL")
        return t

    
    t_NOT = r"\-"
    t_AND = r"&"
    t_OR = r"\|"
    t_IMPLIES = r"=>"
    t_PO = r"\("
    t_PC = r"\)"
    t_COMMA = r"\,"

    t_ignore = " \t\n"

    def t_error(t):
        line = t.value.lstrip()
        i = line.find("\n")
        line = line if i == -1 else line[:i]
        raise ValueError("Syntax error, line {0}: {1}"
                         .format(t.lineno + 1, line))

    def t_newline(t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def p_expression_binary(p):
        """EXPRESSION : EXPRESSION IMPLIES EXPRESSION
                   | EXPRESSION OR EXPRESSION
                   | EXPRESSION AND EXPRESSION"""
        p[0] = [p[1], p[2], p[3]]

    def p_expression_not(p):
        """EXPRESSION : NOT EXPRESSION"""
        p[0] = [p[1], p[2]]

    def p_expression_boolean(p):
        """EXPRESSION : FALSE
                   | TRUE"""
        p[0] = p[1]

    def p_expression_group(p):
        """EXPRESSION : PO EXPRESSION PC"""
        p[0] = p[2]

    def p_expression_symbol(p):
        """EXPRESSION : SYMBOL"""
        p[0] = p[1]


    def p_relation(p):
        """EXPRESSION : SYMBOL PO RELATIONLIST PC"""
        #p[0] = p[1] if len(p) == 2 else [p[1], p[3]]
        p[0] = [p[1],p[3]]
        print(len(p),"r")
    def p_relationlist(p):
        """RELATIONLIST : SYMBOL COMMA RELATIONLIST
                    | SYMBOL"""

        if len(p)==2 :
            p[0] = [p[1]]
        else:
            t = [p[1]]
            t.extend(p[3])
            p[0] = t
        print(len(p), "rl")
    def p_error(p):
        if p is None:
            raise ValueError("Unknown error")
        raise ValueError("Syntax error, line {0}: {1}".format(
            p.lineno + 1, p.type))

    # from lowest to highest precedence!
    precedence = (("right", "IMPLIES"),
                  ("left", "OR"),
                  ("left", "AND"),
                  ("right", "NOT"))

    lexer = lex.lex()
    parser = yacc.yacc()

    return parser.parse(text, lexer=lexer)




def removeImplications(text):
    child = []
    for i in range(len(text)) :
        if type(text[i])== type("str"):
            if(text[i]=="=>"):
                tempNeg = ['-',text[i-1]]
                text[i] = "|"
                text[i-1] = tempNeg
            pass
        else:
            if text[i-1] == "&" or text[i-1] == "|" or text[i-1] == "=>" or text[i-1] == "-" :
                child.append(text[i])
            try:
                if  text[i+1] == "&" or text[i+1] == "|" or text[i+1] == "=>" :
                    child.append(text[i])
            except:
                pass
    for c in child :
        removeImplications(c)
    return text

def moveNegate(text):
    if len(text)==1:
        return text
    if text[0]=="-":
        if len(text[1])==1:
            return text
        elif(len(text[1]))==2:
            notRelation = not (len(text[1]) == 2 and text[1][0] != "-" and type(text[1][1]) == type(["list"]))
            if notRelation:
                return moveNegate(text[1][1])

            else:
                return text
        else:
            for j in range(len(text[1])) :
                if (text[1][j] == "|"):
                    return ([moveNegate(["-", text[1][j - 1]]),"&",moveNegate(["-", text[1][j + 1]])])

                elif (text[1][j] == "&"):
                    return ([moveNegate(["-", text[1][j - 1]]), "|", moveNegate(["-", text[1][j + 1]])])

        return text
    else:
        return text

def toString(text):
    pass
#======================================================================================================================================
print(ply_parse("-(-(b|c))"))
print(removeImplications(ply_parse("a=>b")))
print(moveNegate(ply_parse("-(b&c&d&(S|c&h(a,b,c)))")))



