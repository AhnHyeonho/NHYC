import React, { useState } from "react"
import { Redirect } from "react-router-dom"


// props - login: App.js 에서 signIn function(auth.js)을 호출해서 받은 리턴값을 전달 
function LoginForm({ authenticated, login, location }) {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
 
  // 로그인 버튼 클릭
  const handleClick = () => {
      
    try {
      login({ email, password })

    } catch (e) {
      alert("Failed to login")
      setEmail("")
      setPassword("")
    }

  }

  const { from } = location.state || { from: { pathname: "/" } }
  if (authenticated) return <Redirect to={from} />

  return (
    <>
      <h1>Login</h1>
      <input
        value={email}
        onChange={({ target: { value } }) => setEmail(value)}
        type="text"
        placeholder="email"
      />
      <input
        value={password}
        onChange={({ target: { value } }) => setPassword(value)}
        type="password"
        placeholder="password"
      />
      
      <button onClick={handleClick}>Login</button>
    </>
  )
}

export default LoginForm