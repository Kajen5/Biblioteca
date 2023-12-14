class Calculator(object):
    op = {'*':lambda x,y: x*y,'/':lambda x,y: x/y,'+':lambda x,y: x+y,'-':lambda x,y: x-y}
    def evaluate(self, string):
        d = list(string.replace(" ", ""))
        h = []
        s = ''
        for i in d:
            if i.isdigit() or i == '.':
                s+=i
                continue
            if s != '':
                h.append(float(s))
            s = ''
            h.append(i)
        if s != '':
            h.append(float(s))
        while len(h)> 1:
            print(h)
            h = self.paren(h)
        return h[0]
    def paren(self,d):
        for i in range(len(d)):
            if d[i] == ')':
                for j in range(i):
                    if d[i-j] == '(':
                        print(d[i-j+1:i])
                        d[i-j:i+1] = self.oper(d[i-j+1:i])
                        print(d)
                        return d
                raise "Lacked '(' "
        return self.oper(d)
    def oper(self,s):
        s = self.first(s,['*','/'])
        print(s)
        s = self.first(s,['+','-'])
        return s
    def first(self,s,ope):
        j = 0
        while j < len(s):
            for i in range(len(s)):
                if s[i] in ope:
                    s[i-1:i+2] = [self.op[s[i]](s[i-1],s[i+1])]
                    j = 0
                    break
                j +=1
        return s
if __name__ == '__main__':
    h = Calculator()
    print(h.evaluate("2 / (2 + 3) * 4 - 6"))