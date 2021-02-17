import React from "react"
import { withRouter } from "react-router-dom"

function LogoutButton({ logout, history }) {
  const handleClick = () => {
    logout()
    history.push("/")
  }
  return <button onClick={handleClick}>Logout</button>
}

export default withRouter(LogoutButton)