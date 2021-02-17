import React, { useState } from 'react';
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
import AddressForm from './AddressForm';

import axios from 'axios';
import { TextareaAutosize } from '@material-ui/core';

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
      marginTop: '100px',
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

const steps = ['User Info', 'Prefer Location'];



export default function SignUp() {

  // 하위 컴포넌트 회원가입 페이지 데이터 다루기 위함
  const [id, setId] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [name, setName] = useState('');
  const [sex, setSex] = useState('');
  const [ageGroup, setAgeGroup] = useState('');
  const [monthlyRent, setMonthlyRent] = useState(0);
  const [deposit, setDeposit] = useState(0);

  const [validation, setValidation] = useState({
    isId: false,
    isEmail: false,
    isPassword: false,
    isPasswordConfirm: false,
    isName: false,
    isSex: false,
    isAgeGroup: false,
    isMonthlyRent: false,
    isDeposit: false
  });

  // const handleAgeGroup = (value)=>{
  //   setUser(
  //     { [label] : value }
  //   )
  // }

  // const enabled = 
  //       email.length > 0 && 
  //       password.length > 0 &&
  //       id.length > 0 &&
  //       name.length > 0 &&
  //       sex.length > 0 && 
  //       ageGroup > 0 &&
  //       monthlyRent > 0 &&
  //       deposit > 0;





  const handleId = (value) => {
    setId(value);

    if (value.length > 5) {
      setValidation({
        isId: true,
        isPassword: validation.isPassword,
        isName: validation.isName,
        isSex: validation.isSex,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: validation.isEmail,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    } else {
      setValidation({
        isId: false,
        isPassword: validation.isPassword,
        isName: validation.isName,
        isSex: validation.isSex,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: validation.isEmail,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    }
  }

  const handleEmail = (value) => {
    setEmail(value);

    if (value.length > 5) {
      setValidation({
        isId: validation.isId,
        isPassword: validation.isPassword,
        isName: validation.isName,
        isSex: validation.isSex,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: true,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    } else {
      setValidation({
        isId: validation.isId,
        isPassword: validation.isPassword,
        isName: validation.isName,
        isSex: validation.isSex,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: true,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    }
  }

  const handlePassword = (value) => {
    setPassword(value);
    console.log(value.length)

    if (value.length > 3) {
      setValidation({
        isId: validation.isId,
        isPassword: true,
        isName: validation.isName,
        isSex: validation.isSex,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: validation.isEmail,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    } else {
      setValidation({
        isId: validation.isId,
        isPassword: false,
        isName: validation.isName,
        isSex: validation.isSex,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: validation.isEmail,
        isPasswordConfirm: false,
      })
    }
  }


  const handlePasswordConfirm = (value) => {
    setPasswordConfirm(value);
    if (value === password) {
      console.log("비번 같음")
      setValidation({
        isId: validation.isId,
        isPassword: true,
        isName: validation.isName,
        isSex: validation.isSex,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: validation.isEmail,
        isPasswordConfirm: true
      })
    } else if(password.length != passwordConfirm.length || 
                password !== passwordConfirm) {
      console.log("비번 다름")
      setValidation({
        isId: validation.isId,
        isPassword: true,
        isName: validation.isName,
        isSex: validation.isSex,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: validation.isEmail,
        isPasswordConfirm: false
      })
    }
  }


  const handleName = (value) => {
    setName(value);

    if (value) {
      setValidation({
        isId: validation.isId,
        isPassword: validation.isPassword,
        isName: true,
        isSex: validation.isSex,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: validation.isEmail,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    } else {
      setValidation({
        isId: validation.isId,
        isPassword: validation.isPassword,
        isName: false,
        isSex: validation.isSex,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: validation.isEmail,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    }
  }

  const handleSex = (value) => {
    setSex(value);

    if (value) {
      setValidation({
        isId: validation.isId,
        isPassword: validation.isPassword,
        isName: validation.isName,
        isSex: true,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: validation.isEmail,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    } else {
      setValidation({
        isId: validation.isId,
        isPassword: validation.isPassword,
        isName: validation.isName,
        isSex: false,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: validation.isEmail,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    }
  }

  const handleAgeGroup = (value) => {
    setAgeGroup(value);

    if (value) {
      setValidation({
        isId: validation.isId,
        isPassword: validation.isPassword,
        isName: validation.isName,
        isSex: validation.isSex,
        isAgeGroup: true,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: validation.isEmail,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    } else {
      setValidation({
        isId: validation.isId,
        isPassword: validation.isPassword,
        isName: validation.isName,
        isSex: validation.isSex,
        isAgeGroup: true,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: validation.isEmail,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    }
  }

  const handleMonthlyRent = (value) => {
    setMonthlyRent(value);

    if (value) {
      setValidation({
        isId: validation.isId,
        isPassword: validation.isPassword,
        isName: validation.isName,
        isSex: validation.isSex,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: true,
        isDeposit: validation.isDeposit,
        isEmail: validation.isEmail,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    } else {
      setValidation({
        isId: validation.isId,
        isPassword: validation.isPassword,
        isName: validation.isName,
        isSex: validation.isSex,
        isAgeGroup: true,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: validation.isDeposit,
        isEmail: validation.isEmail,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    }
  }

  const handleDeposit = (value) => {
    setDeposit(value);

    if (value) {
      setValidation({
        isId: validation.isId,
        isPassword: validation.isPassword,
        isName: validation.isName,
        isSex: validation.isSex,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: true,
        isEmail: validation.isEmail,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    } else {
      setValidation({
        isId: validation.isId,
        isPassword: validation.isPassword,
        isName: validation.isName,
        isSex: validation.isSex,
        isAgeGroup: validation.isAgeGroup,
        isMontlyRent: validation.isMonthlyRent,
        isDeposit: true,
        isEmail: validation.isEmail,
        isPasswordConfirm: validation.isPasswordConfirm,
      })
    }
  }


  const handleData = (name, value) => {
    switch (name) {
      case "id":
        handleId(value);
        break;

      case "email":
        handleEmail(value);
        break;

      case "password":
        handlePassword(value);
        break;

      case "passwordConfirm":
        handlePasswordConfirm(value);
        break;

      case "name":
        handleName(value);
        break;

      case "sex":
        handleSex(value);
        break;

      case "ageGroup":
        handleAgeGroup(value);
        break;

      case "monthlyRent":
        handleMonthlyRent(value);
        break;

      case "deposit":
        handleDeposit(value);
        break;
    }
  }
  // const handleAgeGroup = (value)=>{
  //   setUser(
  //     { [label] : value }
  //   )
  // }

  //  ====== 

  const classes = useStyles();
  const [activeStep, setActiveStep] = useState(0);



  function getStepContent(step, validation) {

    switch (step) {
      case 0:
        return <UserInfoSection handleUserInfo={handleData} validation={validation}/>;

      case 1:
        return <AddressForm />;

      default:
        throw new Error('Unknown step');
    }
  }

  const handleNext = () => {

    const btn = document.getElementById('nextbtn').innerHTML;

    console.log(btn)

    if (btn === 'Next') {

      // api호출 =====
      const fetchLabels = async () => {
        try {

          let url = "http://ec2-52-78-44-165.ap-northeast-2.compute.amazonaws.com:8000/api/auth/register/";

          const user = {
            name: name,
            password: password,
            memberId: id,
            email: email,
            gender: sex,
            age_range: ageGroup,
            rentalFee: monthlyRent,
            deposit: deposit
          }

          // request
          const res = axios({
            method: 'post', //put
            url: url,
            data: user
          });

          // const response = await axios.post(url, user);

          console.log(res)




        } catch (e) {
          console.log(e)
        }
      };

      fetchLabels()
      // api 호출 끝 =====
    }

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

                  {getStepContent(activeStep, validation)}

                  <div className={classes.buttons}>
                    {activeStep !== 0 && (
                      <Button onClick={handleBack} className={classes.button}>
                        Back
                      </Button>
                    )}

                    <button
                      id="nextbtn"
                      variant="contained"
                      color="primary"
                      onClick={handleNext}
                      className={classes.button}>
                      {activeStep === steps.length - 1 ? 'Submit' : 'Next'}
                    </button>

                    <div>{id}</div>

                    {console.log(validation)}


                    {/* <Button
                      id="nextbtn"
                      variant="contained"
                      color="primary"
                      onClick={handleNext}
                      className={classes.button}
                    >
                      {activeStep === steps.length - 1 ? 'Submit' : 'Next'}
                    </Button> */}

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