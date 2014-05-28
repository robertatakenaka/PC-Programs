VERSION 5.00
Begin VB.Form JOURNAL5 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Config - Serial's database"
   ClientHeight    =   5460
   ClientLeft      =   45
   ClientTop       =   1335
   ClientWidth     =   7650
   Icon            =   "frm_Serial_7.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   Moveable        =   0   'False
   NegotiateMenus  =   0   'False
   ScaleHeight     =   5460
   ScaleWidth      =   7650
   ShowInTaskbar   =   0   'False
   Begin VB.CommandButton CmdNext 
      Caption         =   "Next"
      Height          =   375
      Left            =   3840
      TabIndex        =   2
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdBack 
      Caption         =   "Back"
      Height          =   375
      Left            =   2760
      TabIndex        =   1
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   6600
      TabIndex        =   4
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdSave 
      Caption         =   "Save"
      Height          =   375
      Left            =   5520
      TabIndex        =   3
      Top             =   5040
      Width           =   975
   End
   Begin VB.Frame Frame1 
      Height          =   975
      Left            =   120
      TabIndex        =   7
      Top             =   3960
      Width           =   7455
      Begin VB.TextBox TxtCprighter 
         Height          =   285
         Left            =   120
         TabIndex        =   0
         Text            =   "Text4"
         Top             =   480
         Width           =   5055
      End
      Begin VB.TextBox TxtCprightDate 
         Height          =   285
         Left            =   5280
         TabIndex        =   8
         Text            =   "Text4"
         Top             =   480
         Visible         =   0   'False
         Width           =   1215
      End
      Begin VB.Label LabCprighter 
         AutoSize        =   -1  'True
         Caption         =   "Copyrighter"
         Height          =   195
         Left            =   120
         TabIndex        =   10
         Top             =   240
         Width           =   795
      End
      Begin VB.Label LabCprightDate 
         AutoSize        =   -1  'True
         Caption         =   "Copyright (Date)"
         Height          =   195
         Left            =   5280
         TabIndex        =   9
         Top             =   240
         Visible         =   0   'False
         Width           =   1140
      End
   End
   Begin VB.Frame FrameCreativeCommons 
      Caption         =   "Creative Commons"
      Height          =   3855
      Left            =   120
      TabIndex        =   6
      Top             =   120
      Width           =   7455
      Begin VB.CommandButton CommandTestLicImgLink 
         Caption         =   "test"
         Height          =   375
         Left            =   6480
         TabIndex        =   19
         Top             =   1680
         Width           =   735
      End
      Begin VB.CommandButton CommandTestLicLink 
         Caption         =   "Test"
         Height          =   375
         Left            =   6480
         TabIndex        =   18
         Top             =   1200
         Width           =   735
      End
      Begin VB.TextBox Text_LicImgLink 
         Height          =   375
         Left            =   1800
         TabIndex        =   17
         Text            =   "Text2"
         Top             =   1680
         Width           =   4575
      End
      Begin VB.TextBox Text_LicLink 
         Height          =   375
         Left            =   1800
         TabIndex        =   16
         Text            =   "Text1"
         Top             =   1200
         Width           =   4575
      End
      Begin VB.ComboBox ComboLicCompl 
         Height          =   315
         Left            =   3120
         TabIndex        =   15
         Text            =   "ComboLicCompl"
         Top             =   720
         Width           =   1335
      End
      Begin VB.ComboBox ComboLicText 
         Height          =   315
         Left            =   120
         TabIndex        =   12
         Text            =   "ComboLicText"
         Top             =   720
         Width           =   1215
      End
      Begin VB.ComboBox ComboLicVersion 
         Height          =   315
         Left            =   1440
         TabIndex        =   11
         Text            =   "Combo1"
         Top             =   720
         Width           =   1575
      End
      Begin VB.Label LabelLicImgLink 
         Caption         =   "Label10"
         Height          =   375
         Left            =   120
         TabIndex        =   21
         Top             =   1560
         Width           =   1575
      End
      Begin VB.Label LabelLicLink 
         Caption         =   "Label10"
         Height          =   375
         Left            =   120
         TabIndex        =   20
         Top             =   1200
         Width           =   1455
      End
      Begin VB.Label LabelLicense 
         Caption         =   "LabelLicense"
         Height          =   375
         Left            =   120
         TabIndex        =   14
         Top             =   480
         Width           =   1215
      End
      Begin VB.Label LabelLicVersion 
         Caption         =   "version de la licencia"
         Height          =   375
         Left            =   1440
         TabIndex        =   13
         Top             =   480
         Width           =   1575
      End
   End
   Begin VB.Label LabIndicationMandatoryField 
      Caption         =   "Label1"
      ForeColor       =   &H000000FF&
      Height          =   255
      Left            =   120
      TabIndex        =   5
      Top             =   5040
      Width           =   2415
   End
End
Attribute VB_Name = "JOURNAL5"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Public IsBack As Boolean
Private MyMfnTitle As Long
Private savedlicense As New clsCreativeCommons
'Private currentLicText As ColIdiom
Private Const MAX_LINES_INDEX = 10
Public interface_cc As New clsCreativeCommons

Private Sub CmdBack_Click()
        Hide
        IsBack = True
        Serial4.MyOpen (MyMfnTitle)
End Sub

Sub MySetLabels()
    
    With Fields
    'LabelCreativeCommonsInstructions.Caption = .getLabel("issue_creativecommons")
    LabCprightDate.Caption = .getLabel("ser4_cprightDate")
    LabCprighter.Caption = .getLabel("ser4_cprighter")
    LabelLicense.Caption = .getLabel("Issue_License")
    LabelLicVersion.Caption = .getLabel("Issue_LicVersion")
    
    Call FillCombo(ComboLicText, CodeLicText, True, True)
    Call FillCombo(ComboLicVersion, CodeLicVersion, True, True)
    ComboLicCompl.Clear
    ComboLicCompl.AddItem ("igo")
    ComboLicCompl.AddItem ("")
    
    End With
    
    With ConfigLabels
        CommandTestLicLink.Caption = .getLabel("ButtonTest")
        CommandTestLicImgLink.Caption = .getLabel("ButtonTest")
        CmdBack.Caption = .getLabel("ButtonBack")
        CmdClose.Caption = .getLabel("ButtonClose")
        CmdSave.Caption = .getLabel("ButtonSave")
        LabIndicationMandatoryField.Caption = .getLabel("MandatoryFieldIndication")
        LabelLicLink.Caption = .getLabel("LicLink")
        LabelLicImgLink.Caption = .getLabel("LicImgLink")
        
    End With
    
End Sub

Sub MyGetContentFromBase(MfnTitle As Long)
    'JournalStatusAction.setLanguage (CurrCodeIdiom)
    'Set JournalStatusAction.ErrorMessages = ErrorMessages
    'Set JournalStatusAction.myHistory = journalDAO.getHistory(MfnTitle)
    Set savedlicense = New clsCreativeCommons
    Set savedlicense = journalDAO.getJournalCreativeCommons(MfnTitle)
    
    If Len(savedlicense.Code) > 0 Then
        ComboLicText.text = savedlicense.Code
    End If
    If Len(savedlicense.version) > 0 Then
        ComboLicVersion.text = savedlicense.version
    Else
        ComboLicVersion.text = ""
    End If
    If Len(savedlicense.COMPLEMENT) > 0 Then
        ComboLicCompl.text = savedlicense.COMPLEMENT
    Else
        ComboLicCompl.text = ""
    End If
    
    TxtCprightDate.text = Serial_TxtContent(MfnTitle, 621)
    TxtCprighter.text = Serial_TxtContent(MfnTitle, 62)

End Sub


Sub MyClearContent()
        TxtCprightDate.text = ""
        TxtCprighter.text = ""
End Sub
Function is_valid_cc() As Boolean
    Dim Msg As String
    If Not interface_cc.is_valid(Msg) Then
        MsgBox (Msg)
        ComboLicText.SetFocus
    End If
    is_valid_cc = True
End Function
Function changed(MfnTitle As Long) As Boolean
    'FIXME
    Dim temp As clsCreativeCommons
    Dim change As Boolean
    
    Set temp = journalDAO.getJournalCreativeCommons(MfnTitle)
    change = (temp.Code <> ComboLicText.text) Or (temp.version <> ComboLicVersion.text)
    
    changed = change
End Function
Sub MyOpen(MfnTitle As Long)
    MyMfnTitle = MfnTitle
    
    Left = FormMenuPrin.SysInfo1.WorkAreaWidth / 2 - (Width + FrmInfo.Width) / 2
    Top = FormMenuPrin.SysInfo1.WorkAreaHeight / 2 - Height / 2
    FrmInfo.Top = Top
    FrmInfo.Left = Left + Width
    
    Show
    'FIXME
    
End Sub

Private Sub CmdCancel_Click()
    CancelFilling
End Sub


Private Sub CmdClose_Click()
    Dim respClose As Integer
    
    respClose = Serial_Close(MyMfnTitle)
    Select Case respClose
    Case 1
        UnloadSerialForms
    Case 2
        CmdSave_Click
        UnloadSerialForms
    End Select
    
End Sub

Private Sub CmdNext_Click()
    SERIAL6.MyOpen (MyMfnTitle)
End Sub

Private Sub CmdSave_Click()
    MousePointer = vbHourglass
    is_valid_cc
    MyMfnTitle = Serial_Save(MyMfnTitle)
    MousePointer = vbArrow
End Sub
Private Sub update_links()
    interface_cc.Code = ComboLicText.text
    interface_cc.version = ComboLicVersion.text
    interface_cc.COMPLEMENT = ComboLicCompl.text
    
    Text_LicLink.text = interface_cc.get_license_link(program_interface_language)
    Text_LicImgLink.text = interface_cc.get_license_img_link(program_interface_language)
End Sub

Private Sub ComboLicCompl_Change()
    update_links
End Sub

Private Sub ComboLicCompl_Click()
update_links
End Sub

Private Sub ComboLicCompl_LostFocus()
update_links
End Sub

Private Sub ComboLicText_Change()
    update_links
End Sub

Private Sub ComboLicText_Click()
update_links
End Sub

Private Sub ComboLicText_LostFocus()
update_links
End Sub

Private Sub ComboLicVersion_Change()
    update_links
End Sub

Private Sub ComboLicVersion_Click()
update_links
End Sub

Private Sub ComboLicVersion_LostFocus()
update_links
End Sub

Private Sub CommandTestLicImgLink_Click()
    Call cmd_exe(Text_LicImgLink.text)
End Sub

Private Sub CommandTestLicLink_Click()
    Call cmd_exe(Text_LicLink.text)
End Sub

Private Sub Form_QueryUnload(Cancel As Integer, UnloadMode As Integer)
    Call FormQueryUnload(Cancel, UnloadMode)
End Sub

Function getCreativeCommons() As clsCreativeCommons
    Set getCreativeCommons = savedlicense
End Function

Private Sub TextCreativeCommons_GotFocus(index As Integer)
Call FrmInfo.ShowHelpMessage(Fields.getLabel("title_creativecommons"), 2)

End Sub
Private Sub TxtCprightDate_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser4_cprightDate")
End Sub

Private Sub TxtCprighter_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser4_cprighter")
End Sub
