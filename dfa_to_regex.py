#Accepts single final state, hence does not add extra start and final states. Simplifies the DFA RegEx at each step of elimination

#Initialize phi and epsilon symbols
phi=chr(934)
eps=chr(949)

#Define closure function
def closure(sym):
    if sym==eps or sym==phi:
        return eps
    elif sym in alpha:
        return (sym+'*')
    else:
        return ('('+sym+')*')

#Define union function for 2 and 3 symbols
def union(sym1,sym2,sym3=None):
    if sym3 is None:
        if sym1==phi:
            return sym2
        elif sym2==phi:
            return sym1
        elif sym1==eps and sym2==eps:
            return eps
        elif sym1==sym2:
            return (sym1)
        else:
            return (sym1+'+'+sym2)
    else:
        if sym1==sym2==sym3:
            return (sym1)
        elif sym1==sym2:
            return (union(sym1,sym3))
        elif sym1==sym3:
            return (union(sym1,sym2))
        elif sym2==sym3:
            return (union(sym1,sym2))
        else:
            return union(sym1,union(sym2,sym3))

#Define concatenation function for 2 and 3 symbols
def concat(sym1,sym2,sym3=None):
    if sym3 is None:
        if sym1==phi or sym2==phi:
            return phi
        elif sym1==eps:
            return sym2
        elif sym2==eps:
            return sym1
        elif '+' not in sym1 and '+' not in sym2:
            return (sym1+'.'+sym2)
        elif '+' not in sym2:
            return ('('+sym1+').'+sym2)
        elif '+' not in sym1:
            return (sym1+'.('+sym2+')')
        else:
            return ('('+sym1+').('+sym2+')')
    else:
        return concat(sym1,concat(sym2,sym3))

#Define eliminate function to eliminate state k
def eliminate(k):
    for i in range(numstates):
        for j in range(numstates):
            dfa[i][i]=union(dfa[i][i],concat(dfa[i][k],closure(dfa[k][k]),dfa[k][i]))
            dfa[j][j]=union(dfa[j][j],concat(dfa[j][k],closure(dfa[k][k]),dfa[k][j]))
            dfa[i][j]=union(dfa[i][j],concat(dfa[i][k],closure(dfa[k][k]),dfa[k][j]))
            dfa[j][i]=union(dfa[j][i],concat(dfa[j][k],closure(dfa[k][k]),dfa[k][i]))

#Define simplify function to simplify RegEx generated at each stage of state elimination
def simplify(st):
    if st.find('(')==-1:
        return ('+'.join(list(set(st.split('+')))))
    else:
        p='+'.join(list(set(st[:st[:st.find('(')].rfind('+')].split('+'))))+st[st[:st.find('(')].rfind('+'):st.find('(')+1]
        q='+'.join(list(set(st[st.find('(')+1:st.find(')')].split('+'))))+')'
        r=st[st.find(')')+1:st[st.find(')'):].find('+')+1]+'+'.join(list(set(st[st[st.find(')'):].find('+')+1:].split('+'))))
        return p+q+r

#Introduction to the project
print('\nTHEORY OF COMPUTATION & COMPILER DESIGN\n')
print('Jagriti wadhwa\t-\t16BCE0998')
print('Deeksha singh \t-\t16BCE0865')
print('Nikita negi\t-\t16BCE2038')
print('       ---------------------------')
print('Welcome!\nThis will convert you DFA to Regular Expression.')
print('Please enter the DFA below as instructed.')
print('       ---------------------------\n')

#Accept the set of alphabets
print('Enter the number of alphabets used: ',end='')
numalpha=int(input())
print('\nEnter the alphabets:')
alpha=[input() for i in range(numalpha)]
alpha.append(eps)

#Accept the number of states
print('\nEnter the number of states in the DFA: ',end='')
numstates=int(input())
print('The states in the DFA run from 0 to',numstates-1)

#Accept the start state
print('\nEnter the start state: ',end='')
start=int(input())

#Accept the final states
print('\nEnter the final state: ',end='')
final=int(input())

#Initialize the DFA with phi
dfa=[[phi for i in range(numstates)] for j in range(numstates)]

#Accept the transitions in DFA and remove multi-ple labels
print('\nEnter the number of transitions in the DFA: ',end='')
numtrans=int(input())
print('\nEnter the transitions, one at a time, in the format:\n<from>,<to>,<alphabet>')
for i in range(numtrans):
    t=input()
    p1=t.find(',')
    p2=t.find(',',p1+1)
    a=t[p2+1:]
    s1=int(t[:p1])
    s2=int(t[p1+1:p2])
    if t[p2+1:] not in alpha:
        print('Incorrect transition alphabet!')
        i-=1
        continue
    elif s1<0 or s1>numstates-1 or s2<0 or s2>numstates-1:
        print('Incorrect transition states!')
        i-=1
        continue
    else:
        dfa[s1][s2]=union(dfa[s1][s2],a)

#Assuming 0: start state, numstates-1: final state
s=start
f=final

#Eliminate all states apart from start and final states and simplify in each stage
for i in range(numstates):
    if i!=s and i!=f:
        eliminate(i)
        for x in range(numstates):
            for y in range(numstates):
                dfa[x][y]=simplify(dfa[x][y])

#Display the final state-eliminated DFA
print('\nThe state-eliminated DFA is:\n',dfa[s],'\n',dfa[f])

#Derive final RegEx and print answer
rex=concat(closure(dfa[s][s]),dfa[s][f],closure(union(concat(dfa[f][s],closure(dfa[s][s]),dfa[s][f]),dfa[f][f])))
print('\nThe regular expression is:\n',rex)

#dfa=[['a.b','a','b+a.a'],['b',phi,'a'],['a+b.b','b','b.a']]
#rex=(a.b)*.((b+a.a).(((a+b.b).((a.b)*.(b+a.a))+b.a)*))
