import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Paper from '@material-ui/core/Paper';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Button from '@material-ui/core/Button';
import Link from '@material-ui/core/Link';
import Typography from '@material-ui/core/Typography';

import UserInfoSection from './UserInfoSection'

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

const useStyles = makeStyles((theme) => ({
  appBar: {
    position: 'relative',
  },
  layout: {
    width: 'auto',
    marginLeft: theme.spacing(2),
    marginRight: theme.spacing(2),
    [theme.breakpoints.up(600 + theme.spacing(2) * 2)]: {
      width: 600,
      marginTop:'100px',
      marginLeft: 'auto',
      marginRight: 'auto',
    },
  },
  paper: {
    marginTop: theme.spacing(3),
    marginBottom: theme.spacing(3),
    padding: theme.spacing(2),
    [theme.breakpoints.up(600 + theme.spacing(3) * 2)]: {
      marginTop: theme.spacing(6),
      marginBottom: theme.spacing(6),
      padding: theme.spacing(3),
    },
  },
  stepper: {
    padding: theme.spacing(3, 0, 5),
  },
  buttons: {
    display: 'flex',
    justifyContent: 'flex-end',
  },
  button: {
    marginTop: theme.spacing(3),
    marginLeft: theme.spacing(1),
  },
  success: {
    marginTop: theme.spacing(3),
  }
}));

const steps = ['User Info'];

function getStepContent(step) {
  switch (step) {
    case 0:
      return <UserInfoSection />;
    // case 1:
    //   return <PaymentForm />;
    // case 2:
    //   return <Review />;
    default:
      throw new Error('Unknown step');
  }
}

export default function SignUp() {
  const classes = useStyles();
  const [activeStep, setActiveStep] = React.useState(0);

  const handleNext = () => {
    setActiveStep(activeStep + 1);
  };

  const handleBack = () => {
    setActiveStep(activeStep - 1);
  };

  return (

    <React.Fragment>
      <CssBaseline />
    
      <main className={classes.layout}>
        
        <Paper className={classes.paper}>
          
          {/* 상단 타이틀  */}
          <Typography component="h1" variant="h4" align="center">
            Sign Up
          </Typography>

          {/* 입력 form */}
          <React.Fragment>

            {/* 제출하기 버튼 눌렀을 때 */}
            {activeStep === steps.length ? (
              <React.Fragment>

                <Typography className={classes.success} variant="h5" gutterBottom >
                  축하합니다!
                </Typography>

                <Typography variant="subtitle1">
                  회원가입이 완료되었습니다. 
                </Typography>
                
                <Button
                    href="map"
                    variant="contained"
                    color="primary"
                    className={classes.button}
                  >
                    Home
                  </Button>
              </React.Fragment>
            ) : (
              <React.Fragment>

                {getStepContent(activeStep)}

                <div className={classes.buttons}>
                  {activeStep !== 0 && (
                    <Button onClick={handleBack} className={classes.button}>
                      Back
                    </Button>
                  )}

                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleNext}
                    className={classes.button}
                  >
                    {activeStep === steps.length - 1 ? 'Submit' : 'Next'}
                  </Button>

                </div>
              </React.Fragment>
            )}

          </React.Fragment>

        </Paper>
        <Copyright />
      </main>
    </React.Fragment>
  );
}