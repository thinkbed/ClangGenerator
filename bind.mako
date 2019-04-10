
void testClass(lua_State* L)
{
% for c in classes:
    % if c.brief_comment == "SCRIPT_ACCESSABLE":
    registerClass<${c.name}>(L, "${c.name}");
    % for f in c.functions:
        % if not "hidden" in f.annotations:
        registerClassFunction<${c.name}>(L, "${f.name}", &${c.name}::${f.name});
        % endif
    % endfor
    % for v in c.member_variables:
        % if not "hidden" in v.annotations:
        registerClassMemberVariable<${c.name}>(L, "${v.name}", &${c.name}::${v.name});
        % endif
    % endfor

    % endif
% endfor
}

