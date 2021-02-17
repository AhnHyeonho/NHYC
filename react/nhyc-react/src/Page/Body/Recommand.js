import React from 'react';


function Recommand ({user}){
    const { email, password, name } = user || {}

    return(
        <>
            <h1>Profile</h1>
            <dt>Email</dt>
            <dd>{email}</dd>
            <dt>Password</dt>
            <dd>{password}</dd>
            <dt>Name</dt>
            <dd>{name}</dd>
        </>
    
    
    )
}


export default Recommand;