import React, { useState } from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import { LoginPage } from '../..';
import { Redirect } from "react-router-dom"


function Copyright() {
    return (
        <Typography variant="body2" color="textSecondary" align="center">
            {'Copyright © '}
            <Link color="inherit" href="https://material-ui.com/">
                Your Website
      </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}

const styles = theme => ({
    paper: {
        // marginTop: theme.spacing(8),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    avatar: {
        // margin: theme.spacing(1),
        // backgroundColor: theme.palette.secondary.main,
    },
    form: {
        width: '100%', // Fix IE 11 issue.
        // marginTop: theme.spacing(1),
    },
    submit: {
        // margin: theme.spacing(3, 0, 2),
    },
});

function Login({ authenticated, login, location }) {

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


    const { from } = location.state || { from: { pathname: "/recommand" } }
    if (authenticated) return <Redirect to={from} />

    const classes = styles();

    return (
        <Container component="main" maxWidth="xs" style={{ "margin-top": "50px" }}>
            <CssBaseline />
            <div className={classes.paper} style={{ 'text-align': "center" }}>
                <Avatar className={classes.avatar} style={{ 'text-align': "center", 'display': "inline-flex" }}>
                    <LockOutlinedIcon />
                </Avatar>
                <Typography component="h1" variant="h5">
                    Sign in
        </Typography>
                <form className={classes.form} noValidate>
                    <TextField
                        variant="outlined"
                        margin="normal"
                        required
                        fullWidth
                        id="email"
                        label="Email Address"
                        name="email"
                        autoComplete="email"
                        autoFocus

                        value={email}
                        onChange={({ target: { value } }) => setEmail(value)}
                    />
                    <TextField
                        variant="outlined"
                        margin="normal"
                        required
                        fullWidth
                        name="password"
                        label="Password"
                        type="password"
                        id="password"
                        autoComplete="current-password"

                        value={password}
                        onChange={({ target: { value } }) => setPassword(value)}
                    />
                    {/* <FormControlLabel
                            control={<Checkbox value="remember" color="primary" />}
                            label="Remember me"
                        /> */}

                    <div style={{ 'height': "20px" }}></div>

                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="primary"
                        className={classes.submit}
                        onClick={handleClick}
                    >
                        Sign In
                        </Button>

                    <Grid container>
                        <Grid item xs>
                            {/* <Link href="#" variant="body2">
                                    Forgot password?
              </Link> */}
                        </Grid>
                        <Grid item style={{ "margin-top": "10px" }}>
                            <Link href="#" variant="body2">
                                {"Don't have an account? Sign Up"}
                            </Link>
                        </Grid>
                    </Grid>
                </form>
            </div>
            <Box mt={8}>
                <Copyright />
            </Box>
        </Container>
    );
}


export default Login;