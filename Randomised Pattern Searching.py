from cmath import log
import random
import math

def power(m,n,q):
    if n==0:
        return 1
    else:
        return (m*power(m,n-1,q)%q)
#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

def modPatternMatch(q,p,x):
    n=len(x)#computing length of pattern and text
    m=len(p)
    h=power(26,m-1,q) 
    p1=0
    t1=0
    ans=[]
    for i in range (0,m):
        p1=(26*p1+ord(p[i]))%q #calculating the 26-ary representation of pattern 
        t1=(26*t1+ord(x[i]))%q #calculating the 26-ary representation of first m characters of text time
    for s in range (0,n-m+1):#checking for each window in text of size m, if it's hash value is equal to hash value of pattern
        if p1==t1: 
            ans.append(s) #if yes, append to list
        if s<n-m:
            t1=(26*(t1-ord(x[s])*h)+ord(x[s+m]))%q#shift the window by on eunit, subtract the 26-ary value of first value of previous window and add the last+1 value's 26-ary representation.
            if t1<0:
                t1=t1+q
    return ans#returns the final list.

 #SPACE COMPLEXITY:
 #Since we are taking mod q at every step, max value of the remainder can be q-1, hence max number of bits stored is logq.
 #In the loop, the max value of s can be n, so number of bits stored =logn
 #length of ans list=k
 #hence total space complexity=O(k+logn+logq)
 #TIME COMPLEXITY:
 #max number of iterations are m+n and since we are storing remainders of q, max bits can be logq and each bitwise operation takes O(1).HEnce time complexity-O((m+n)*logq)
def modPatternMatchWildcard(q,p,x):
    n=len(x)
    m=len(p)
    h=power(26,m-1,q)
    p1=0
    t1=0
    ans=[]
    index=0
    for i in range (0,m):#finding the index of "?" in pattern
        if p[i]=="?":
            index=i
    current=index
    for i in range (0,m):
        p1=(26*p1+(ord(p[i])))%q
        t1=(26*t1+ord(x[i]))%q
    p1=(p1-pow(26,m-index-1)*ord(p[index])+pow(26,m-index-1)*ord("A"))%q #changing the "?" to "A"'s hash value in the fuction (eg if pattern is "D?" then this hash value is for "DA")
    t1=(t1-pow(26,m-index-1)*ord(x[index])+pow(26,m-index-1)*ord("A"))%q #changing the character in text at index-current to "A" (for above example, if text is ABCDE, then hash value is for AACDE)
    for s in range (0,n-m+1):
        if p1==t1: 
            ans.append(s)#if hash value same, append
        t1=(t1+pow(26,m-current-1)*ord(x[index])-pow(26,m-current-1)*ord("A"))%q #changing the hash value of text to the original one
        index=index+1#appending the index by 1 as we are rolling the window 
        if s<n-m:
            t1=((26*(t1-ord(x[s])*h)+ord(x[s+m]))-pow(26,m-current-1)*ord(x[index])+pow(26,m-current-1)*ord("A"))%q #changing the charcter at index current of the window to "A" and computing the hash value. 
            if t1<0:
                t1=t1+q
       
    return ans
#since modpatternmatchwildcard follows the same idea as modpatternmatch, only a few additions that take constant space and spice, it's space and time complexity is the same as that of modpatternmatch. i.e
#space complexity-O(k+logn+logq) time complexity-O((m+n)*logq)

def findN(eps,m):
    N=int(pow(((2*m*log(26))/eps),2))
#Why this N?
#Let a=hash value of text
#b=hash value of pattern
#for a false positive, a!=b but a mod q=b mod q. 
#i.e q|(|a-b|).
#P(false positive)<=eps
#P(false positive)=summation over all possible (|a-b|=d)*(No of q s.t q|(|a-b|)/No of primes till N)
#Max number of q that can divide 26^m is log(26^m)=m*log(26)
#m*log(26)/(N/2*logn)<=eps (no of primes till N=N/2*logN)
#i.e N/logN>=(2m*log26)/eps
#since N/logN>=sqroot(N)
#so I took N as such.
#time complexity- O(no of bits)=O(N)=O(log(m/eps)), space complexity=no of bits stored=O(log(m/eps))
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)
#findN takes O()log(m/eps) time  space
#here q will be of the form m/eps
#modpatternmatch time-O((m+n)*logq) and space-O(k+logn+logq)
#hence, randpatternmatch has time complexity-O((m+n)*log(m/eps)) and space complexity-O(k+logn+log(m/eps))

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)
#follows from the explanation of findN, modpatternmatchwildcard and randpatternmatch.
# time and space complexity is same as that of randpatternmatch.	




    