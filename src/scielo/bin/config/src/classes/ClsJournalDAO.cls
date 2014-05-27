VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsJournalDAO"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Private isis As ClIsisdll
Const changelinetextbox = vbCrLf

Function getJournalStandardList() As MyCollection
    Dim journals As New MyCollection
    Dim journal As ClsJournal
    Dim pissn As String
    Dim eissn As String
    
    Dim i As Long
    
    For i = 1 To isis.MfnQuantity
        Set journal = New ClsJournal
        
        journal.is_published = isis.FieldContentOccGet(i, 50, 1)
        
        journal.ISSN = isis.FieldContentOccGet(i, 400, 1)
        journal.shorttitle = isis.FieldContentOccGet(i, 150, 1)
        journal.JournalStandard = isis.FieldContentOccGet(i, 117, 1)
        journal.MedlineTitle = isis.FieldContentOccGet(i, 421, 1)
        journal.pmid = isis.FieldContentOccGet(i, 420, 1)
        
        
        Call serial_issn_get(i, pissn, eissn)
        journal.print_issn = pissn
        journal.online_issn = eissn
        
        journal.publisherName = isis.UsePft(i, "(v480+|, |)")
        journal.SUBJECT = isis.UsePft(i, "(v441+|/|)")
        journal.fulltitle = isis.FieldContentOccGet(i, 100, 1)
        journal.acron = isis.FieldContentOccGet(i, 68, 1)
        
        
        Call journals.add(journal, journal.ISSN + journal.shorttitle)
    Next
    Set getJournalStandardList = journals
End Function

Function getHistory(Mfn As Long) As ClsHistory
    Dim q As Long
    Dim occs() As String
    Dim i As Long
    Dim journalStatus As ClsJournalStatus
    Dim history As New ClsHistory
    
    
    
    q = isis.FieldContentGetAll(Mfn, 51, occs)
    For i = q To 1 Step -1
        Set journalStatus = New ClsJournalStatus
        
        journalStatus.statusDate = isis.getSubfieldContent("a", occs(i))
        journalStatus.status = isis.getSubfieldContent("b", occs(i))
        
        Call history.add(journalStatus, journalStatus.statusDate)
        
        If InStr(occs(i), "^c") > 0 Then
            Set journalStatus = New ClsJournalStatus
            journalStatus.statusDate = isis.getSubfieldContent("c", occs(i))
            journalStatus.status = isis.getSubfieldContent("d", occs(i))
            
            Call history.add(journalStatus, journalStatus.statusDate)
        End If
        
    Next
    Set getHistory = history
End Function
Function tagHistory(history As ClsHistory) As String
    Dim i As Long
    
    Dim journalStatus As ClsJournalStatus
    
    Const tag = "51"
    Dim tagged As String
    Dim Occ As String
    
    
    For i = 1 To history.count
        Set journalStatus = history.item(i)
        If Len(Occ) = 0 Then
            Occ = "<" + tag + ">^a" + journalStatus.statusDate + "^b" + journalStatus.status
        Else
            Occ = Occ + "^c" + journalStatus.statusDate + "^d" + journalStatus.status + "</" + tag + ">"
            tagged = Occ + tagged
            Occ = ""
        End If
    Next
    If Len(Occ) > 0 Then
        Occ = Occ + "</" + tag + ">"
        tagged = Occ + tagged
    End If
    
    tagHistory = tagged
End Function

Function getJournalCreativeCommons(Mfn As Long) As clsCreativeCommons
    Dim languages() As String
    Dim texts() As String
    Dim creativeCommons As New clsCreativeCommons
        
    creativeCommons.Code = Serial_TxtContent(Mfn, 541)
    creativeCommons.version = Serial_TxtContent(Mfn, 542)
    
    Set getJournalCreativeCommons = creativeCommons
End Function
Function tagCreativeCommons(lic As String, lic_version As String) As String
    Dim i As Long
    Const tag = "540"
    Dim tagged As String
    
    If lic = "nd" Then
        tagged = tagged + "<" + tag + ">^t<p></p>^len</" + tag + ">"
        tagged = tagged + "<" + tag + ">^t<p></p>^les</" + tag + ">"
        tagged = tagged + "<" + tag + ">^t<p></p>^lpt</" + tag + ">"
    ElseIf lic = "" Then
    
    Else
        Call license_locations(lic, lic_version, license_location, license_img_location)
        If Len(license_location) > 0 Then
            tagged = tagged + "<" + tag + ">^t" + get_license(license_location, license_img_location, "en") + "^len</" + tag + ">"
            tagged = tagged + "<" + tag + ">^t" + get_license(license_location, license_img_location, "es") + "^les</" + tag + ">"
            tagged = tagged + "<" + tag + ">^t" + get_license(license_location, license_img_location, "pt") + "^lpt</" + tag + ">"
        End If
    End If
    tagCreativeCommons = tagged
End Function
Private Function get_license(license_location As String, license_img_location As String, lang As String) As String
    Dim link As String
    Dim text As String
    Dim translation As String
    
    Select Case lang
    Case "pt"
        translation = "deed.pt"
        link = license_link("Atributição de Licença Creative Commons", license_location & translation)
        text = "Todo o conteúdo deste periódico, exceto onde está identificado, está baixo uma "
    Case "en"
        translation = ""
        link = license_link("Creative Commons Attribution License", license_location)
        text = "All the contents of this journal, except where otherwise noted, is licensed under a "
    Case "es"
        translation = "deed.es"
        link = license_link("Atribución de Licencia Creative Commons", license_location & translation)
        text = "Todo el contenido de esta revista, excepto dónde está identificado, está bajo una "
    End Select
    get_license = license_link(license_img(license_img_location) & text & link, license_location & translation)
End Function
Private Function format_attribute(name As String, value As String) As String
    format_attribute = " " & name & "=" & Chr(34) & value & Chr(34)
End Function

Private Function format_attribute(name As String, value As String) As String
    format_attribute = " " & name & "=" & Chr(34) & value & Chr(34)
End Function

Private Sub license_locations(lic As String, lic_version As String, ByRef license_location As String, ByRef license_img_location As String)
    license_location = "http://creativecommons.org/licenses/" & LCase(lic) & "/" & lic_version & "/"
    license_img_location = "http://i.creativecommons.org/l/" & LCase(lic) & "/" & lic_version & "/80x15.png"
End Sub

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


Private Sub Class_Initialize()
    Set isis = New ClIsisdll
    
    With Paths("Title Database")
    If isis.Inicia(.Path, .FileName, .key) Then
        If isis.IfCreate(Paths("Title X ISSN Database").FileName) Then
            
        End If
    End If
    End With
End Sub

Function save(ByRef MfnTitle As Long, Data As String) As Boolean
    Dim OK As Boolean
    If MfnTitle = 0 Then
         MfnTitle = isis.RecordSave(Data)
         OK = (MfnTitle > 0)
    Else
        OK = isis.RecordUpdate(MfnTitle, Data)
    End If

    If OK Then
        Call isis.IfUpdate(MfnTitle, MfnTitle)
    End If
    save = OK
End Function

Function getJournalList() As ClsJournalList
    Dim i As Long
    Dim tmp As String
    Dim j As ClsJournal
    Dim jlist As New ClsJournalList
    
    For i = 1 To isis.MfnQuantity
        tmp = isis.UsePft(i, "v400,' ',v100")
        If Len(tmp) > 0 Then
            Set j = New ClsJournal
            j.key = tmp
            j.Title = Mid(tmp, 11)
            j.ISSN = Mid(tmp, 1, 9)
            j.pubid = isis.UsePft(i, "v68")
            j.CollectionURL = isis.UsePft(i, "v690")
            j.JournalStandard = isis.UsePft(i, "v117")
            j.shorttitle = isis.UsePft(i, "v150")
            Call jlist.add(j)
        End If
    Next
    Set getJournalList = jlist
End Function


Function existJournal(journalKey As String, journalTitle As String) As Long
    Dim i As Long
    Dim j As Long
    
    i = existJournalTitle(journalTitle)
    j = existISSN(journalKey)
    If i = j Then
    
    Else
        
    End If
End Function

Function existRecord(key As String, format As String, Optional Prefix As String) As Long
    Dim MfnCounter As Long
    Dim mfns() As Long
    Dim i As Long
    Dim found As Boolean
    Dim value As String
    Dim ID As String
    Dim Mfn As Long
    
    ID = key
    If Len(key) > 30 Then key = Mid(Prefix + key, 1, 30)
    MfnCounter = isis.MfnFind(key, mfns)
    
    i = 0
    While (i < MfnCounter) And (Not found)
        i = i + 1
        value = isis.UsePft(mfns(i), format)
        If StrComp(value, ID) = 0 Then
            Mfn = mfns(i)
            found = True
        End If
    Wend
    
    If Not found Then
        i = 0
        While (i < isis.MfnQuantity) And (Not found)
            i = i + 1
            value = isis.UsePft(Mfn, format)
            If StrComp(Trim(value), Trim(ID)) = 0 Then
                found = True
                Mfn = i
            End If
        Wend
    End If
    existRecord = Mfn
End Function

Function existJournalTitle(journalTitle As String) As Long
    existJournalTitle = existRecord(journalTitle, "v100")
End Function
Function existISSN(journal_ISSN As String) As Long
    existISSN = existRecord(journal_ISSN, "v400", "pbn=")
End Function

Function getFieldContentByLanguage(Mfn As Long, tag As Long, Optional language As String) As String
    Dim subf As String
    If language <> "" Then subf = "*"
    
    getFieldContentByLanguage = isis.getFieldContentByLanguage(Mfn, tag, language, subf)
End Function

Function getDecodedValue(Code As ColCode, Mfn As Long, tag As Long, Optional DefaultOption As String) As String
    Dim content As String
    Dim exist As Boolean
    Dim itemCode As ClCode
    
        content = isis.UsePft(Mfn, "v" + CStr(tag))
        If (Len(content) = 0) And (Len(DefaultOption) > 0) Then content = DefaultOption
        
        If Len(content) > 0 Then
            Set itemCode = New ClCode
            Set itemCode = Code(content, exist)
            If exist Then
                content = itemCode.value
            Else
                Debug.Print
            End If
        End If
    getDecodedValue = content
End Function

Function getRepetitiveFieldValue(Mfn As Long, tag As Long, sep As String) As String
     getRepetitiveFieldValue = isis.UsePft(Mfn, "(v" + CStr(tag) + "|" + sep + "|)")
End Function

Function delete(journal_ISSN As String) As Boolean
    Dim Mfn As Long
    Dim issueDAO As New ClsIssueDAO
    Dim issueMFNs() As Long
    Dim i As Long
    Dim r As Boolean
    
    With Paths("Issue Database")
    Set issueDAO = New ClsIssueDAO
    Call issueDAO.create(.Path, .FileName, .key)
    End With
    
    Mfn = existRecord(journal_ISSN, "v400", "pbn=")
    If Mfn > 0 Then
        issueMFNs = issueDAO.getIssuesMfnByJournalID(journal_ISSN)
        For i = 1 To UBound(issueMFNs)
            r = issueDAO.deleteRecord(issueMFNs(i))
        Next
        r = isis.RecordDel(Mfn)
        'r = save(mfn, "d*")
    End If
    delete = r
End Function
