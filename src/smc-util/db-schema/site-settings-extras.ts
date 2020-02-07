// config for server settings, which are only visible and editable for admins. in particular, this includes the email backend config.

import {
  Config,
  only_for_smtp,
  only_for_sendgrid,
  only_for_password_reset_smtp,
  to_bool,
  only_booleans,
  to_int
} from "./site-defaults";

// not public, but admins can edit them
export const EXTRAS: { [key: string]: Config } = {
  email_backend: {
    name: "Email backend type",
    desc: "enter the type of backend, 'none' means there is none",
    default: "",
    valid: ["none", "sendgrid", "smtp"]
  },
  sendgrid_key: {
    name: "Sendgrid API key",
    desc: "You need a Sendgrid account and then enter a valid API key here",
    default: "",
    show: only_for_sendgrid
  },
  email_smtp_server: {
    name: "SMTP server",
    desc: "the hostname to talk to",
    default: "",
    show: only_for_smtp
  },
  email_smtp_login: {
    name: "SMTP username",
    desc: "the username, for PLAIN login",
    default: "",
    show: only_for_smtp
  },
  email_smtp_password: {
    name: "SMTP password",
    desc: "the password, for PLAIN login",
    default: "",
    show: only_for_smtp,
    password: true
  },
  email_smtp_port: {
    name: "SMTP port",
    desc: "Usually: For secure==true use port 465, otherwise port 587 or 25",
    default: "465",
    to_val: to_int,
    show: only_for_smtp
  },
  email_smtp_secure: {
    name: "SMTP secure",
    desc: "Usually 'true'",
    default: "true",
    valid: only_booleans,
    to_val: to_bool,
    show: only_for_smtp
  },
  password_reset_override: {
    name: "Password reset backend",
    desc:
      "If 'default', it uses the usual email backend to send password resets. If 'smtp', an additional SMTP config shows up",
    default: "default",
    valid: ["default", "smtp"]
  },
  password_reset_smpt_server: {
    name: "PW reset SMTP server",
    desc: "hostname sending password reset emails",
    default: "",
    show: only_for_password_reset_smtp
  },
  password_reset_smpt_login: {
    name: "PW reset SMTP username",
    desc: "username, PLAIN auth",
    default: "",
    show: only_for_password_reset_smtp
  },
  password_reset_smpt_password: {
    name: "PW reset SMTP password",
    desc: "password, PLAIN auth",
    default: "",
    show: only_for_password_reset_smtp,
    password: true
  },
  password_reset_smpt_port: {
    name: "PW reset SMTP port",
    desc: "Usually: For secure==true use port 465, otherwise port 587 or 25",
    default: "465",
    to_val: to_int,
    show: only_for_password_reset_smtp
  },
  password_reset_smpt_secure: {
    name: "PW reset SMTP secure",
    desc: "Usually 'true'",
    default: "true",
    valid: only_booleans,
    to_val: to_bool,
    show: only_for_password_reset_smtp
  }
} as const;
