int koh551(int izz890, int grh682) {
    int _f0_state = 0;
    int hlh858;
_f0_dispatcher:
    switch (_f0_state) {
        case 0: goto _f0_case_0;
        case 1: goto _f0_case_1;
        case 2: goto _f0_end;
    }
    {
    _f0_case_0:
        hlh858 = (izz890 - (-grh682));
        _f0_state = 1;
        goto _f0_dispatcher;
    }
    {
    _f0_case_1:
        return hlh858;
    }
    {
    _f0_end:
        return 0;
    }
}
int main() {
    int _f1_state = 0;
    int fzs308;
    int qkv5;
    int rxh531;
    int unused_0;
    int unused_1;
    int unused_2;
_f1_dispatcher:
    switch (_f1_state) {
        case 0: goto _f1_case_0;
        case 1: goto _f1_case_1;
        case 2: goto _f1_case_2;
        case 3: goto _f1_case_3;
        case 4: goto _f1_case_4;
        case 5: goto _f1_case_5;
        case 6: goto _f1_case_6;
        case 7: goto _f1_case_7;
        case 8: goto _f1_end;
    }
    {
    _f1_case_0:
        unused_0 = 582;
        _f1_state = 1;
        goto _f1_dispatcher;
    }
    {
    _f1_case_1:
        fzs308 = 3;
        _f1_state = 2;
        goto _f1_dispatcher;
    }
    {
    _f1_case_2:
        rxh531 = 4;
        _f1_state = 3;
        goto _f1_dispatcher;
    }
    {
    _f1_case_3:
        unused_1 = 170;
        _f1_state = 4;
        goto _f1_dispatcher;
    }
    {
    _f1_case_4:
        qkv5 = koh551(fzs308, rxh531);
        _f1_state = 5;
        goto _f1_dispatcher;
    }
    {
    _f1_case_5:
        unused_2 = 141;
        _f1_state = 6;
        goto _f1_dispatcher;
    }
    {
    _f1_case_6:
        printf("%d\n", qkv5);
        _f1_state = 7;
        goto _f1_dispatcher;
    }
    {
    _f1_case_7:
        return 0;
    }
    {
    _f1_end:
        return 0;
    }
}