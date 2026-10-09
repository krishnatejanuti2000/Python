test_results = ["LoginTest:Pass","PaymentTest:Fail","LogoutTest:Pass","SignupTest:Fail"]

result = []

for i in test_results:
    name, status = i.split(":")

    if status == "Fail":
        result.append(name)

if result:
    print("Failed test cases:")

    for i in result:
        print(i)

    print(f"\nTotal failed tests: {len(result)}")

else:
    print("No failed test cases.")