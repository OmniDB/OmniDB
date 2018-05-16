#ifdef _MSC_VER
#ifdef _M_X64
#pragma comment( linker, "/export:_PG_init" )
#pragma comment( linker, "/export:omnidb_enable_debugger" )
#else
#pragma comment( linker, "/export:__PG_init" )
#pragma comment( linker, "/export:_omnidb_enable_debugger" )
#endif
#endif

extern void _PG_init(void);