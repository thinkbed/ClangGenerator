
#ifdef __CODE_GENERATOR__
#define HIDDEN __attribute__((annotate("hidden")))
#define SCRIPT __attribute__((annotate("script")))
#else
#define HIDDEN
#define SCRIPT
#endif

SCRIPT int g_gloabl_context;

//! SCRIPT_ACCESSABLE
class A
{
public:
    A() { _a = 100; }

    const char* is_base() { return "this is base class A"; }
    
    int _a;
};

//! SCRIPT_ACCESSABLE
class B : public A
{
private:
    float getF() {return _f;}

public:
    B(int val) : _b(val) {}
    ~B() {}

    const char* is_derived() { return "this is derived class B"; }

    HIDDEN int ret_b() { return _b; }
    int ret_mulb(int m) { return _b*m; }
    X getX() { return X(_b); }
    void setX(X x) { _b = x.value; }

    int _b;
    HIDDEN float _f;
};

void testClass(lua_State* L)
{
    registerClass<A>(L, "A");
    registerClassFunction<A>(L, "is_base", &A::is_base);
    registerClassMemberVariable<A>(L, "_a", &A::_a);

    registerClass<B>(L, "B");
    inherientClass<B, A>(L);
    addClassConstructor<B>(L, constructor<B, int>);
    registerClassFunction<B>(L, "is_derived", &B::is_derived);
    registerClassFunction<B>(L, "ret_b", &B::ret_b);
    registerClassFunction<B>(L, "ret_mulb", &B::ret_mulb);
    registerClassFunction<B>(L, "getX", &B::getX);
    registerClassFunction<B>(L, "setX", &B::setX);
    registerClassMemberVariable<B>(L, "_b", &B::_b);

    registerVariable(L, "g_cb", &g_cb);

    B cb(2048);
    registerVariable(L, "local_cb", &cb);

    dofile(L, "example3.lua");

    B& lb = getVariable<B&>(L, "lb");

    printf("get local lb from lua: lb._b = %d\n", lb._b);
}
