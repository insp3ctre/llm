from functions.get_files_info import get_files_info

res = get_files_info("calculator", ".")
print(f"""
Result for current directory:
{res}
""")

res = get_files_info("calculator", "pkg")
print(f"""
Result for 'pkg" directory:
{res}
""")

res = get_files_info("calculator", "/bin")
print(f"""
Result for '/bin':
{res}
""")

res = get_files_info("calculator", "../")
print(f"""
Result for '../' directory:
{res}
""")