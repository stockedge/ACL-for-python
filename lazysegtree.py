class lazy_segtree():
    n=1
    size=2
    log=2
    e=0
    op=None
    mapping=None
    composition=None
    identity=None
    d=[]
    lz=[]
    def __init__(self,V,OP,E,MAPPING,COMPOSITION,ID):
        self.op=OP
        self.e=E
        self.mapping=MAPPING
        self.composition=COMPOSITION
        self.identity=ID
        
        self.n=len(V)
        self.log=(self.n-1).bit_length()
        self.size=1<<self.log
        self.d=[self.e for i in range(2*self.size)]
        self.lz=[self.identity for i in range(self.size)]
        for i in range(self.n):
            self.d[self.size+i]=V[i]
        for i in range(self.size-1,0,-1):
            self.update(i)
    def set(self,p,x):
        assert 0<=p and p<self.n
        p+=self.size
        for i in range(self.log,0,-1):
            self.push(p>>i)
        self.d[p]=x
        for i in range(1,self.log+1):
            self.update(p>>i)
    def get(self,p):
        assert 0<=p and p<self.n
        p+=self.size
        for i in range(self.log,0,-1):
            self.push(p>>i)
        return self.d[p]
    def prod(self,l,r):
        assert 0<=l and l<=r and r<=self.n
        if l==r:
            return self.e
        l+=self.size
        r+=self.size
        for i in range(self.log,0,-1):
            if (((l>>i)<<i)!=l):
                self.push(l>>i)
            if (((r>>i)<<i)!=r):
                self.push(r>>i)
        sml=self.e
        smr=self.e
        while(l<r):
            if (l&1):
                sml=self.op(sml,self.d[l])
                l+=1
            if (r&1):
                r-=1
                smr=self.op(self.d[r],smr)
            l>>=1
            r>>=1
        return self.op(sml,smr)
    def all_prod(self):
        return self.d[1]
    def apply(self,*args):
        if len(args)==2:
            p=args[0];f=args[1]
            assert 0<=p and p<self.n
            p+=self.size
            for i in range(self.log,0,-1):
                self.push(p>>i)
            self.d[p]=mapping(f,d[p])
            for i in range(1,self.log+1):
                self.update(p>>i)
        else:
            l=args[0];r=args[1];f=args[2]
            assert 0<=l and l<=r and r<=self.n
            if l==r:
                return
            l+=self.size
            r+=self.size
            for i in range(self.log,0,-1):
                if (((l>>i)<<i)!=l):
                    self.push(l>>i)
                if (((r>>i)<<i)!=r):
                    self.push((r-1)>>i)
            l2=l;r2=r
            while(l<r):
                if (l&1):
                    self.all_apply(l,f)
                    l+=1
                if (r&1):
                    r-=1
                    self.all_apply(r,f)
                l>>=1
                r>>=1
            l=l2
            r=r2
            for i in range(1,self.log+1):
                if (((l>>i)<<i)!=l):
                    self.update(l>>i)
                if (((r>>i)<<i)!=r):
                    self.update((r-1)>>i)
    def max_right(self,l,g):
        assert 0<=l and l<=self.n
        assert g(self.e)
        if l==self.n:
            return self.n
        l+=self.size
        for i in range(self.log,0,-1):
            self.push(l>>i)
        sm=self.e
        while(1):
            while(i%2==0):
                l>>=1
            if not(g(self.op(sm,self.d[l]))):
                while(l<self.size):
                    self.push(l)
                    l=(2*l)
                    if (g(self.op(sm,self.d[l]))):
                        sm=self.op(sm,self.d[l])
                        l+=1
                return l-self.size
            sm=self.op(sm,self.d[l])
            l+=1
            if (l&-l)==l:
                break
        return self.n
    def min_left(self,r,g):
        assert (0<=r and r<=self.n)
        assert g(self.e)
        if r==0:
            return 0
        r+=self.size
        for i in range(self.log,0,-1):
            self.push((r-1)>>i)
        sm=self.e
        while(1):
            r-=1
            while(r>1 and (r%2)):
                r>>=1
            if not(g(self.op(self.d[r],sm))):
                while(r<self.size):
                    self.push(r)
                    r=(2*r+1)
                    if g(self.op(self.d[r],sm)):
                        sm=self.op(self.d[r],sm)
                        r-=1
                return r+1-self.size
            sm=self.op(self.d[r],sm)
            if (r&-r)==r:
                break
        return 0
    def update(self,k):
        self.d[k]=self.op(self.d[2*k],self.d[2*k+1])
    def all_apply(self,k,f):
        self.d[k]=self.mapping(f,self.d[k])
        if (k<self.size):
            self.lz[k]=self.composition(f,self.lz[k])
    def push(self,k):
        self.all_apply(2*k,self.lz[k])
        self.all_apply(2*k+1,self.lz[k])
        self.lz[k]=self.identity