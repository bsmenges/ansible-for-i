#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Le Chang <changle@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_user_and_group
short_description: Create, Change or Display a user(or group) profile
version_added: 2.10
description:
  - The C(ibmi_user_and_group) module can do the user(or group) profile management(create, change, delete and display).
  - A user profile contain a user's passwords, the list of special authorities assigned to a user, and the objects the user owns.
  - A group profile is a special type of user profile that provides the same authority to a group of users.
  - You create group profiles in the same way that you create individual profiles.
  - The system recognizes a group profile when you add the first member to it.
  - At that point, the system sets information in the profile indicating that it is a group profile.
options:
  operation:
    description:
      - The user or group profile operation.
      - Operation create to create user(group) profile
      - Operation change to change user(group) profile
      - Operation display to display user(group) profile inforamtion
      - Operation display_group_menbers to display the members of a group profile
    choices: ['create', 'change', 'delete', 'display', 'display_group_members']
    type: str
    required: yes
  user:
    description:
      - Specifies the user profile to be created. A numeric user profile can be specified.
      - If the user profile begins with a numeric, it must be prefixed with a Q.
      - If you want to create, display, display group members of a group, this parameter is the group profile name.
    type: str
    required: yes
  password:
    description:
      - Specifies the password that allows the user to sign on the system.
      - If not specify, operation create will use the user name as the password, operation change will not change the password.
    type: str
    default: '*SAME'
  expire:
    description:
      - Specifies whether the password for this user is set to expired.
      - If the password is set to expired, the user is required to change the password to sign on the system.
      - If not specify, '*NO' will be used for operation create, '*SAME' will be used for operation change.
    type: str
    choices: ['*NO', '*YES', '*SAME']
    default: '*SAME'
  status:
    description:
      - Specifies the status of the user profile.
      - If not specify, '*ENABLED' will be used for operation create, '*SAME' will be used for operation change.
    type: str
    choices: ['*ENABLED', '*DISABLED', '*SAME']
    default: '*SAME'
  user_class:
    description:
      - Specifies the type of user associated with this user profile, security officer, security administrator, programmer, system operator, or user.
      - If not specify, '*USER' will be used for operation create, '*SAME' will be used for operation change.
    type: str
    choices: ['*USER', '*SYSOPR', '*PGMR','*SECADM', '*SECOFR', '*SAME']
    default: '*SAME'
  special_authority:
    description:
      - Specifies the special authorities given to a user.
      - If not specify, '*USRCLS' will be used for operation create, '*SAME' will be used for operation change.
    type: list
    elements: str
    choices: ['*USRCLS', '*NONE', '*SAME',
        '*ALLOBJ', '*AUDIT', '*JOBCTL', '*SAVSYS', '*IOSYSCFG', '*SECADM', '*SERVICE', '*SPLCTL']
    default: ['*SAME']
  user_group:
    description:
      - Specifies the user's group profile name whose authority is used if no specific authority is given for the user.
      - If not specify, operation create is to create an individual user, or else, the new created user will be a member of the group.
      - If not specify, operation change does nothing on the user, or else, the new changed user will be added as a member of the group.
    type: str
    default: '*SAME'
  owner:
    description:
      - Specifies the user that is to be the owner of objects created by this user.
      - If not specify, '*USRPRF' will be used for operation create, '*SAME' will be used for operation change.
    type: str
    choices: ['*USRPRF', '*GRPPRF', '*SAME']
    default: '*SAME'
  text:
    description:
      - Specifies the text that briefly describes the user or group profile.
      - If not specify, 'Create by Ansible' will be used for operation create, '*SAME' will be used for operation change.
    type: str
    default: '*SAME'
  parameters:
    description:
      - The parameters that CRTUSRPRF or CHGUSRPRF command will take.
      - Other than options above, all other parameters need to be specified here.
      - The default values of parameters for CRTUSRPRF or CHGUSRPRF will be taken if not specified.
      - Supported parameters contain
      - ASTLVL, CURLIB, INLPGM, INLMNU, LMTCPB, TEXT, SPCENV, DSPSGNINF, PWDEXPITV, PWDCHGBLK, LCLPWDMGT, LMTDEVSSN, KBDBUF, MAXSTGLRG, MAXSTG, PTYLMT,
      - GRPAUT, GRPAUTTYP, SUPGRPPRF, ACGCDE, DOCPWD, MSGQ, DLVRY, SEV, PRTDEV, OUTQ, ATNPGM, SRTSEQ, LANGID, CNTRYID, CCSID, CHRIDCTL, SETJOBATR,
      - LOCALE, USROPT, UID, GID, HOMEDIR, EIMASSOC, USREXPDATE, USREXPITV, AUT, JOBD when the operation is create or change
      - Or OWNOBJOPT, PGPOPT, EIMASSOC when the operation is delete.
      - refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/crtusrprf.htm.
      - and https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/dltusrprf.htm for detail.
    type: str
    default: ' '
notes:
    - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)

seealso:
- module: ibmi_cl_command

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: create user profile
  ibmi_user_and_group:
    operation: 'create'
    user: 'changle'

- name: display user profile
  ibmi_user_and_group:
    operation: 'display'
    user: 'changle'

- name: display group members
  ibmi_user_and_group:
    operation: 'display_group_members'
    user: 'group1'
'''

RETURN = r'''
sstdout:
    description: The standard output
    returned: when rc as 0(success) and the operation is not display or display_group_members
    type: str
    sample: "CPC2205: User profile CHANGLE changed."
stderr:
    description: The standard error
    returned: when rc as no-zero(failure)
    type: str
    sample: 'CPF22CF: User profile not allowed to be a group profile'
rc:
    description: The return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 255
stdout_lines:
    description: The command standard output split in lines
    returned: when rc as 0(success) and the operation is not display or display_group_members
    type: list
    sample: [
        "CPC2205: User profile CHANGLE changed."
    ]
stderr_lines:
    description: The command standard error split in lines
    returned: when rc as no-zero(failure)
    type: list
    sample: [
        "CPF2204: User profile CHANGL1 not found."
    ]
result_set:
    description: The result set of user information or group members
    returned: When rc as 0(success) and operation is display or display_group_members
    type: list
    sample: [
        {
            "GROUP_PROFILE_NAME": "GROUP1",
            "USER_PROFILE_NAME": "USERG1",
            "USER_TEXT": ""
        },
        {
            "GROUP_PROFILE_NAME": "GROUP1",
            "USER_PROFILE_NAME": "USER2G1",
            "USER_TEXT": ""
        }
    ]
'''

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common import validation

try:
    from shlex import quote
except ImportError:
    from pipes import quote

HAS_ITOOLKIT = True
HAS_IBM_DB = True

try:
    import ibm_db_dbi as dbi
except ImportError:
    HAS_IBM_DB = False

try:
    from itoolkit import iToolKit
    from itoolkit import iSqlFree
    from itoolkit import iSqlFetch
    from itoolkit import iSqlQuery
    from itoolkit import iCmd
    from itoolkit import iCmd5250
    from itoolkit.transport import DatabaseTransport
    from itoolkit.transport import DirectTransport
except ImportError:
    HAS_ITOOLKIT = False

try:
    import ibm_db_dbi as dbi
except ImportError:
    HAS_IBM_DB = False

IBMi_COMMAND_RC_SUCCESS = 0
IBMi_COMMAND_RC_UNEXPECTED = 999
IBMi_COMMAND_RC_ERROR = 255
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG = 256
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR = 257


def interpret_return_code(rc):
    if rc == IBMi_COMMAND_RC_SUCCESS:
        return 'Success'
    elif rc == IBMi_COMMAND_RC_ERROR:
        return 'Generic failure'
    elif rc == IBMi_COMMAND_RC_UNEXPECTED:
        return 'Unexpected error'
    elif rc == IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG:
        return "iToolKit result dict does not have key 'joblog'"
    elif rc == IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR:
        return "iToolKit result dict does not have key 'error'"
    else:
        return "Unknown error"


def itoolkit_run_command(command, asp_group):
    conn = dbi.connect()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    if asp_group != '':
        itransport = DirectTransport()
        itool.add(iCmd('command', "SETASPGRP ASPGRP({asp_group_pattern})".format(asp_group_pattern=asp_group), {'error': 'on'}))
    itool.add(iCmd('command', command, {'error': 'on'}))
    itool.call(itransport)

    out = ''
    err = ''

    if asp_group != '' and isinstance(itool.dict_out('command'), list) and len(itool.dict_out('command')) > 1:
        command_output = itool.dict_out('command')[1]
    else:
        command_output = itool.dict_out('command')

    if 'success' in command_output:
        rc = IBMi_COMMAND_RC_SUCCESS
        out = command_output['success']
    elif 'error' in command_output:
        command_error = command_output['error']
        if 'joblog' in command_error:
            rc = IBMi_COMMAND_RC_ERROR
            err = command_error['joblog']
        else:
            # should not be here, must xmlservice has internal error
            rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG
            err = "iToolKit result dict does not have key 'joblog', the output is %s" % command_output
    else:
        # should not be here, must xmlservice has internal error
        rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR
        err = "iToolKit result dict does not have key 'error', the output is %s" % command_output

    return rc, out, err


def itoolkit_run_sql(sql, db):
    if db.strip() != '':
        try:
            conn = dbi.connect(database='{db_pattern}'.format(db_pattern=db))
        except Exception as e:
            out_list = []
            err = "%s, most likely the database does not exist on the system" % str(e)
            rc = IBMi_COMMAND_RC_UNEXPECTED
            return rc, out_list, err
    else:
        conn = dbi.connect()

    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(iSqlQuery('query', sql, {'error': 'on'}))
    itool.add(iSqlFetch('fetch'))
    itool.add(iSqlFree('free'))
    itool.call(itransport)

    command_output = itool.dict_out('fetch')

    out_list = []
    out = ''
    err = ''
    if 'error' in command_output:
        command_error = command_output['error']
        if 'joblog' in command_error:
            rc = IBMi_COMMAND_RC_ERROR
            err = command_error['joblog']
        else:
            # should not be here, must xmlservice has internal error
            rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG
            err = "iToolKit result dict does not have key 'joblog', the output is %s" % command_output
            if 'Row not found' in err:
                rc = 0  # treat as success but also indicate the Row not found message in stderr
    else:
        rc = IBMi_COMMAND_RC_SUCCESS
        out = command_output['row']
        if isinstance(out, dict):
            out_list.append(out)
        elif isinstance(out, list):
            out_list = out

    return rc, out_list, err


def main():
    module = AnsibleModule(
        argument_spec=dict(
            operation=dict(type='str',
                           choices=['create', 'change', 'display', 'delete', 'display_group_members'],
                           required=True),
            user=dict(type='str', required=True),
            password=dict(type='str', default='*SAME', no_log=True),
            expire=dict(type='str', choices=['*YES', '*NO', '*SAME'], default='*SAME'),
            status=dict(type='str', choices=['*ENABLED', '*DISABLED', '*SAME'], default='*SAME'),
            user_class=dict(type='str', choices=['*USER', '*SYSOPR', '*PGMR', '*SECADM', '*SECOFR', '*SAME'], default='*SAME'),
            special_authority=dict(type='list',
                                   choices=['*USRCLS', '*NONE', '*SAME',
                                            '*ALLOBJ', '*AUDIT', '*JOBCTL', '*SAVSYS', '*IOSYSCFG', '*SECADM', '*SERVICE', '*SPLCTL'],
                                   default=['*SAME'],
                                   elements='str'),
            user_group=dict(type='str', default='*SAME'),
            owner=dict(type='str', choices=['*USRPRF', '*GRPPRF', '*SAME'], default='*SAME'),
            text=dict(type='str', default='*SAME'),
            parameters=dict(type='str', default=' '),
        ),
        supports_check_mode=True,
    )

    operation = module.params['operation'].strip()
    user = module.params['user'].strip().upper()
    if len(user) > 10:
        module.fail_json(rc=256, msg="Value of user exceeds 10 characters")
    password = module.params['password']
    expire = module.params['expire'].strip().upper()
    status = module.params['status'].strip().upper()
    user_class = module.params['user_class'].strip().upper()
    special_authority = module.params['special_authority']
    special_authority = [item.strip().upper() for item in special_authority]
    user_group = module.params['user_group'].strip().upper()
    if len(user_group) > 10:
        module.fail_json(rc=256, msg="Value of user_group exceeds 10 characters")
    owner = module.params['owner'].strip().upper()
    text = module.params['text'].strip().upper()
    parameters = module.params['parameters'].strip().upper()

    # handle value for special_authority
    if isinstance(special_authority, list) and len(special_authority) > 1:
        single_value = ['*USRCLS', '*NONE', '*SAME']
        for item in single_value:
            if item in special_authority:
                module.fail_json(rc=256, msg="{p_item} must be only value for parameter special_authority".format(p_item=item))

    # handle parameter special_authority
    authorities = ''
    for item in special_authority:
        authorities = authorities + ' ' + item
    authorities = authorities.strip().upper()

    # convert default value for operation create
    if operation == 'create':
        if password == '' or password.strip().upper() == '*SAME':
            password = '*USRPRF'
        if expire == '' or expire == '*SAME':
            expire = '*NO'
        if status == '' or status == '*SAME':
            status = '*ENABLED'
        if user_class == '' or user_class == '*SAME':
            user_class = '*USER'
        if authorities == '' or authorities == '*SAME':
            authorities = '*USRCLS'
        if user_group == '' or user_group == '*SAME':
            user_group = '*NONE'
        if owner == '' or owner == '*SAME':
            owner = '*USRPRF'
        if text == '' or text == '*SAME':
            text = 'Create by Ansible'

    # Check to see if the group exists
    chkobj_cmd = 'QSYS/CHKOBJ OBJ(QSYS/{p_group}) OBJTYPE(*USRPRF)'.format(p_group=user_group)
    args = ['system', chkobj_cmd]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc != 0:
        group_exist = False
    else:
        group_exist = True

    # Check to see if the user exists
    chkobj_cmd = 'QSYS/CHKOBJ OBJ(QSYS/{p_user}) OBJTYPE(*USRPRF)'.format(p_user=user)
    args = ['system', chkobj_cmd]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc != 0:
        user_exist = False
    else:
        user_exist = True

    if operation == 'create':
        if user_exist:
            module.fail_json(rc=256, msg="User profile {p_user} already exists".format(p_user=user))
        if (user_group != '*NONE') and (not group_exist):
            module.fail_json(rc=256, msg="Group profile {p_group} not found".format(p_group=user_group))

        command = "CRTUSRPRF USRPRF({p_user}) PASSWORD({p_password}) PWDEXP({p_expire}) STATUS({p_status})\
            USRCLS({p_class}) SPCAUT({p_special}) GRPPRF({p_group}) OWNER({p_owner}) TEXT('{p_text}') {parameters}".format(
            p_user=user, p_password=password, p_expire=expire, p_status=status,
            p_class=user_class, p_special=authorities, p_group=user_group, p_owner=owner, p_text=text, parameters=parameters)

    elif operation == 'change':
        if not user_exist:
            module.fail_json(rc=256, msg="User profile {p_user} not found".format(p_user=user))
        if (user_group != '*NONE') and (user_group != '*SAME') and (not group_exist):
            module.fail_json(rc=256, msg="Group profile {p_group} not found".format(p_group=user_group))

        command = "CHGUSRPRF USRPRF({p_user}) PASSWORD({p_password}) PWDEXP({p_expire}) STATUS({p_status})\
            USRCLS({p_class}) SPCAUT({p_special}) GRPPRF({p_group}) OWNER({p_owner}) TEXT('{p_text}') {parameters}".format(
            p_user=user, p_password=password, p_expire=expire, p_status=status,
            p_class=user_class, p_special=authorities, p_group=user_group, p_owner=owner, p_text=text, parameters=parameters)

    elif operation == 'delete':
        if not user_exist:
            module.fail_json(rc=256, msg="User profile {p_user} not found".format(p_user=user))
        command = 'DLTUSRPRF USRPRF({p_user}) {parameters}'.format(p_user=user, parameters=parameters)

    elif operation == 'display':
        if not user_exist:
            module.fail_json(rc=256, msg="User {p_user} not found".format(p_user=user))
        command = "SELECT * FROM QSYS2.USER_INFO WHERE AUTHORIZATION_NAME = '{p_user}'".format(p_user=user)

    else:
        # operation == 'display_group_members'
        if not user_exist:
            module.fail_json(rc=256, msg="Group profile {p_user} not found".format(p_user=user))
        command = 'SELECT * FROM QSYS2.GROUP_PROFILE_ENTRIES'

    if operation == 'display' or operation == 'display_group_members':
        if HAS_ITOOLKIT is False:
            module.fail_json(rc=999, msg="itoolkit package is required")

        if HAS_IBM_DB is False:
            module.fail_json(rc=999, msg="ibm_db package is required")

        rc, out, err = itoolkit_run_sql(command, '')
    else:
        args = ['system', command]
        rc, out, err = module.run_command(args, use_unsafe_shell=False)

    rc_msg = interpret_return_code(rc)
    if operation == 'display' or operation == 'display_group_members':
        if rc != IBMi_COMMAND_RC_SUCCESS:
            result_failed = dict(
                stdout=out,
                stderr=err,
                command=command,
                rc=rc,
            )
            message = 'non-zero return code:{rc},{rc_msg}'.format(
                rc=rc, rc_msg=rc_msg)
            module.fail_json(msg=message, **result_failed)
        else:
            result_success = dict(
                result_set=out,
                command=command,
                rc=rc,
            )
            module.exit_json(**result_success)
    else:
        if rc != IBMi_COMMAND_RC_SUCCESS:
            result_failed = dict(
                command=command,
                stderr=err,
                rc=rc,
            )
            message = 'non-zero return code:{rc},{rc_msg}'.format(rc=rc, rc_msg=rc_msg)
            module.fail_json(msg=message, **result_failed)
        else:
            result_success = dict(
                command=command,
                stdout=out,
                rc=rc,
                changed=True,
            )
            module.exit_json(**result_success)


if __name__ == '__main__':
    main()
