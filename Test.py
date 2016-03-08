import StringBuilder as sb

def testString(str):
    str += "method"
    print "method called"

print "HelloWorld"
str = sb.StringBuilder()
str += "Testing"
str += "does " + "this " + "work?"
testString(str)
print str
