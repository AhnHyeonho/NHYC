const users = [
    { email: "kim", password: "123", name: "Kim" },
    { email: "lee@test.com", password: "456", name: "Lee" },
    { email: "park@test.com", password: "789", name: "Park" },
]

// 여기서 api로 로그인 로직 처리하면 될 듯 
export function signIn({ email, password }) {
    const user = users.find(
        (user) => user.email === email && user.password === password
    )
    if (user === undefined) {
        console.log("로그인 안된다")


        throw new Error()
    }

    
    return user
}