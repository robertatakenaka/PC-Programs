VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "clsCreativeCommons"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Public Code As String
Public version As String
Public COMPLEMENT As String

Function get_license_html(lang As String) As String
    Dim html_img As String
    Dim html_text As String
    Dim html_link_text As String
    Dim lic_location As String
    Dim text As String
    Dim deed As String
    
    deed = get_deed(lang)
    html_img = license_img(license_img_location(deed))
    html_text = license_text1(lang)
    html_link_text = license_text2(lang)
    lic_location = license_location(deed)
    text = html_img & html_text & license_link(html_link_text, lic_location)
    get_license_html = license_link(text, lic_location)
End Function
Function get_license_link(lang As String) As String
    get_license_link = license_location(get_deed(lang))
End Function
Function get_license_img_link(lang As String) As String
    get_license_img_link = license_img_location(get_deed(lang))
End Function
Private Function get_deed(lang As String) As String
    Dim deed As String

    Select Case lang
    Case "en"
        deed = ""
    Case Else
        deed = "deed." & lang & "/"
    End Select
    get_deed = deed
End Function
Private Function format_attribute(name As String, value As String) As String
    format_attribute = " " & name & "=" & Chr(34) & value & Chr(34)
End Function
Private Function replace_text(text As String, Optional deed As String = "") As String
    If Code <> "nd" Then
        replace_text = Replace(Replace(Replace(Replace(text, "<LIC>", LCase(Code)), "<LIC_VERSION>", version), "<IGO>", COMPLEMENT), "<LANG>", deed)
    End If
End Function
Private Function license_text1(lang As String) As String
    license_text1 = ConfigLabels.getLabel(lang & "_license_text1")
End Function
Private Function license_text2(lang As String) As String
    license_text2 = replace_text(ConfigLabels.getLabel(lang & "_license_text2"))
End Function
Private Function license_location(deed As String) As String
    license_location = replace_text(ConfigLabels.getLabel("license_template"), deed)
End Function
Private Function license_img_location(deed As String) As String
    license_img_location = replace_text(ConfigLabels.getLabel("license_img_template"), deed)
End Function
Private Function license_link(text As String, href As String) As String
    Dim tag As String
    
    tag = "<a "
    tag = tag & format_attribute("rel", "license")
    tag = tag & format_attribute("href", href)
    tag = tag & ">"
    
    tag = tag & text
    tag = tag & "</a>"
    license_link = tag
End Function

Private Function license_img(img_src As String) As String
    Dim img As String
    
    img = "<img "
    img = img & format_attribute("alt", "Creative Commons License")
    img = img & format_attribute("style", "border-width:0")
    img = img & format_attribute("src", img_src)
    img = img & "/>"
    license_img = img
End Function

Function is_valid(ByRef Msg As String) As Boolean
    Dim r As Boolean
    Msg = ""
    r = True
    If Code = "" Then
        r = False
        Msg = ConfigLabels.getLabel("msg_missing_license")
        
    ElseIf Code = "nd" Then
        If version <> "nd" Then
            r = False
            Msg = ConfigLabels.getLabel("msg_missing_license_version")
        End If
    Else
        If version = "" Or version = "nd" Then
            r = False
            Msg = ConfigLabels.getLabel("msg_missing_license_version")
        End If
    End If
    is_valid = r
End Function

Function tagged() As String
    Dim r As String
    Dim Msg As String
    
    Const tag = "540"
    
    If Code = "nd" Then
        r = r + "<" + tag + ">^t<p></p>^len</" + tag + ">"
        r = r + "<" + tag + ">^t<p></p>^les</" + tag + ">"
        r = r + "<" + tag + ">^t<p></p>^lpt</" + tag + ">"
    ElseIf Code = "" Then
    
    Else
        If is_valid(Msg) Then
            r = r + "<" + tag + ">^t" + get_license_html("en") + "^len</" + tag + ">"
            r = r + "<" + tag + ">^t" + get_license_html("es") + "^les</" + tag + ">"
            r = r + "<" + tag + ">^t" + get_license_html("pt") + "^lpt</" + tag + ">"
        End If
    End If
    If Len(r) > 0 Then
        r = r + "<541>" + Code + "</541>"
        If Len(COMPLEMENT) > 0 Then
            r = r + "<542>^v" + version + "^c" + COMPLEMENT + "</542>"
        Else
            r = r + "<542>^v" + version + "</542>"
        End If
    End If
    tagged = r
End Function

