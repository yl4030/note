#!/bin/bash
KUBE_PS1_NS_COLOR="${KUBE_PS1_NS_COLOR-cyan}"
KUBE_PS1_CONTEXT_COLOR="${KUBE_PS1_CONTEXT_COLOR-red}"
GIT_BRANCH_COLOR="${GIT_BRANCH_COLOR-yellow}"
KUBE_PS1_SHELL="bash"
_kube_ps1_init() {
      _KUBE_PS1_OPEN_ESC=$'\001'
      _KUBE_PS1_CLOSE_ESC=$'\002'
      _KUBE_PS1_DEFAULT_BG=$'\033[49m'
      _KUBE_PS1_DEFAULT_FG=$'\033[39m'
}

_kube_ps1_init


_kube_ps1_color_fg() {
  local KUBE_PS1_FG_CODE
  case "${1}" in
    black) KUBE_PS1_FG_CODE=0;;
    red) KUBE_PS1_FG_CODE=1;;
    green) KUBE_PS1_FG_CODE=2;;
    yellow) KUBE_PS1_FG_CODE=3;;
    blue) KUBE_PS1_FG_CODE=4;;
    magenta) KUBE_PS1_FG_CODE=5;;
    cyan) KUBE_PS1_FG_CODE=6;;
    white) KUBE_PS1_FG_CODE=7;;
    # 256
    [0-9]|[1-9][0-9]|[1][0-9][0-9]|[2][0-4][0-9]|[2][5][0-6]) KUBE_PS1_FG_CODE="${1}";;
    *) KUBE_PS1_FG_CODE=default
  esac

  if [[ "${KUBE_PS1_FG_CODE}" == "default" ]]; then
    KUBE_PS1_FG_CODE="${_KUBE_PS1_DEFAULT_FG}"
    return
  elif [[ "${KUBE_PS1_SHELL}" == "zsh" ]]; then
    KUBE_PS1_FG_CODE="%F{$KUBE_PS1_FG_CODE}"
  elif [[ "${KUBE_PS1_SHELL}" == "bash" ]]; then
    if tput setaf 1 &> /dev/null; then
      KUBE_PS1_FG_CODE="$(tput setaf ${KUBE_PS1_FG_CODE})"
    elif [[ $KUBE_PS1_FG_CODE -ge 0 ]] && [[ $KUBE_PS1_FG_CODE -le 256 ]]; then
      KUBE_PS1_FG_CODE="\033[38;5;${KUBE_PS1_FG_CODE}m"
    else
      KUBE_PS1_FG_CODE="${_KUBE_PS1_DEFAULT_FG}"
    fi
  fi
  echo ${_KUBE_PS1_OPEN_ESC}${KUBE_PS1_FG_CODE}${_KUBE_PS1_CLOSE_ESC}
}

_kube_ps1_color_bg() {
  local KUBE_PS1_BG_CODE
  case "${1}" in
    black) KUBE_PS1_BG_CODE=0;;
    red) KUBE_PS1_BG_CODE=1;;
    green) KUBE_PS1_BG_CODE=2;;
    yellow) KUBE_PS1_BG_CODE=3;;
    blue) KUBE_PS1_BG_CODE=4;;
    magenta) KUBE_PS1_BG_CODE=5;;
    cyan) KUBE_PS1_BG_CODE=6;;
    white) KUBE_PS1_BG_CODE=7;;
    # 256
    [0-9]|[1-9][0-9]|[1][0-9][0-9]|[2][0-4][0-9]|[2][5][0-6]) KUBE_PS1_BG_CODE="${1}";;
    *) KUBE_PS1_BG_CODE=$'\033[0m';;
  esac

  if [[ "${KUBE_PS1_BG_CODE}" == "default" ]]; then
    KUBE_PS1_FG_CODE="${_KUBE_PS1_DEFAULT_BG}"
    return
  elif [[ "${KUBE_PS1_SHELL}" == "zsh" ]]; then
    KUBE_PS1_BG_CODE="%K{$KUBE_PS1_BG_CODE}"
  elif [[ "${KUBE_PS1_SHELL}" == "bash" ]]; then
    if tput setaf 1 &> /dev/null; then
      KUBE_PS1_BG_CODE="$(tput setab ${KUBE_PS1_BG_CODE})"
    elif [[ $KUBE_PS1_BG_CODE -ge 0 ]] && [[ $KUBE_PS1_BG_CODE -le 256 ]]; then
      KUBE_PS1_BG_CODE="\033[48;5;${KUBE_PS1_BG_CODE}m"
    else
      KUBE_PS1_BG_CODE="${DEFAULT_BG}"
    fi
  fi
  echo ${OPEN_ESC}${KUBE_PS1_BG_CODE}${CLOSE_ESC}
}

__kube_ps1()
{
    # Get current context
#    CONTEXT=$(cat ~/.kube/config | grep "current-context:" | sed "s/current-context: //")
    KUBE_PS1=""
    NAMESPACE=$(kubectl config view --minify --output 'jsonpath={..namespace}' 2>/dev/null)
    CONTEXT=$(kubectl config current-context)
    #GIT_BRANCH=$(git describe --contains --all HEAD 2>/dev/null)
    GIT_BRANCH=$(git symbolic-ref HEAD 2>/dev/null  | cut -d/ -f3) 
   if [ -n "$CONTEXT" ]; then
        #echo "(k8s: ${CONTEXT})"
        KUBE_PS1+="$(_kube_ps1_color_fg ${KUBE_PS1_CONTEXT_COLOR})k8s: ${CONTEXT}"
    fi
    if [ -n "${NAMESPACE}" ];then
       KUBE_PS1+=" |$(_kube_ps1_color_fg ${KUBE_PS1_NS_COLOR}) ns: ${NAMESPACE}${KUBE_PS1_RESET_COLOR}"
    fi
   
    if [ -n "${GIT_BRANCH}" ];then
       KUBE_PS1+=" |$(_kube_ps1_color_fg ${GIT_BRANCH_COLOR}) git: ${GIT_BRANCH}${KUBE_PS1_RESET_COLOR}"
    fi
    echo -e "(${KUBE_PS1})"
}
