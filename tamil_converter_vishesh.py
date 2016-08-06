#!/usr/bin/python
# -*- coding: utf-8 -*-

#Source: http://www.tamillexicon.com/uc/bamini-unicode

import os, sys
import getopt


def writeTamil(t):

    text = t;
    
    
    
    text = text.replace("sp", "ளி");
    
    text = text.replace("hp", "ரி");
    
    text = text.replace("hP", "ரீ");
    
    text = text.replace("uP", "ரீ");
    
    text = text.replace("u;", "ர்");
    
    text = text.replace("h;", "ர்");
    
    text = text.replace("H", "ர்");
    
    
    
    
    
    
    
    text = text.replace("nfs", "கௌ");
    
    text = text.replace("Nfh", "கோ");
    
    text = text.replace("nfh", "கொ");
    
    text = text.replace("fh", "கா");
    
    text = text.replace("fp", "கி");
    
    text = text.replace("fP", "கீ");
    
    text = text.replace("F", "கு");
    
    text = text.replace("$", "கூ");
    
    text = text.replace("nf", "கெ");
    
    text = text.replace("Nf", "கே");
    
    text = text.replace("if", "கை");
    
    text = text.replace("f;", "க்");
    
    text = text.replace("f", "க");
    
    
    
    text = text.replace("nqs", "ஙௌ");
    
    text = text.replace("Nqh", "ஙோ");
    
    text = text.replace("nqh", "ஙொ");
    
    text = text.replace("qh", "ஙா");
    
    text = text.replace("qp", "ஙி");
    
    text = text.replace("qP", "ஙீ");
    
    text = text.replace("nq", "ஙெ");
    
    text = text.replace("Nq", "ஙே");
    
    text = text.replace("iq", "ஙை");
    
    text = text.replace("q;", "ங்");
    
    text = text.replace("q", "ங");
    
    
    
    text = text.replace("nrs", "சௌ");
    
    text = text.replace("Nrh", "சோ");
    
    text = text.replace("nrh", "சொ");
    
    text = text.replace("rh", "சா");
    
    text = text.replace("rp", "சி");
    
    text = text.replace("rP", "சீ");
    
    text = text.replace("R", "சு");
    
    text = text.replace("#", "சூ");
    
    text = text.replace("nr", "செ");
    
    text = text.replace("Nr", "சே");
    
    text = text.replace("ir", "சை");
    
    text = text.replace("r;", "ச்");
    
    text = text.replace("r", "ச");
    
    
    
    
    
    
    
    text = text.replace("n[s", "ஜௌ");
    
    text = text.replace("N[h", "ஜோ");
    
    text = text.replace("n[h", "ஜொ");
    
    text = text.replace("[h", "ஜா");
    
    text = text.replace("[p", "ஜி");
    
    text = text.replace("[P", "ஜீ");
    
    text = text.replace("[{", "ஜு");
    
    text = text.replace("[_", "ஜூ");
    
    
    
    text = text.replace("n[", "ஜெ");
    
    text = text.replace("N[", "ஜே");
    
    text = text.replace("i[", "ஜை");
    
    text = text.replace("[;", "ஜ்");
    
    text = text.replace("[", "ஜ");
    
    
    
    
    
    
    
    
    
    
    
    text = text.replace("nQs", "ஞௌ");
    
    text = text.replace("NQh", "ஞோ");
    
    text = text.replace("nQh", "ஞொ");
    
    text = text.replace("Qh", "ஞா");
    
    text = text.replace("Qp", "ஞி");
    
    text = text.replace("QP", "ஞீ");
    
    text = text.replace("nQ", "ஞெ");
    
    text = text.replace("NQ", "ஞே");
    
    text = text.replace("iQ", "ஞை");
    
    text = text.replace("Q;", "ஞ்");
    
    text = text.replace("Q", "ஞ");
    
    
    
    text = text.replace("nls", "டௌ");
    
    text = text.replace("Nlh", "டோ");
    
    text = text.replace("nlh", "டொ");
    
    text = text.replace("lp", "டி");
    
    text = text.replace("lP", "டீ");
    
    text = text.replace("lh", "டா");
    
    text = text.replace("b", "டி");
    
    text = text.replace("B", "டீ");
    
    text = text.replace("L", "டு");
    
    text = text.replace("\^", "டூ");
    
    text = text.replace("nl", "டெ");
    
    text = text.replace("Nl", "டே");
    
    text = text.replace("il", "டை");
    
    text = text.replace("l;", "ட்");
    
    text = text.replace("l", "ட");
    
    
    
    text = text.replace("nzs", "ணௌ");
    
    text = text.replace("Nzh", "ணோ");
    
    text = text.replace("nzh", "ணொ");
    
    text = text.replace("zh", "ணா");
    
    text = text.replace("zp", "ணி");
    
    text = text.replace("zP", "ணீ");
    
    
    
    
    
    text = text.replace("Zh", "ணூ");
    
    text = text.replace("Z}", "ணூ");
    
    
    
    text = text.replace("nz", "ணெ");
    
    text = text.replace("Nz", "ணே");
    
    text = text.replace("iz", "ணை");
    
    
    
    
    
    text = text.replace("z;", "ண்");
    
    text = text.replace("Z", "ணு");
    
    text = text.replace("z", "ண");
    
    
    
    
    
    
    
    text = text.replace("njs", "தௌ");
    
    text = text.replace("Njh", "தோ");
    
    text = text.replace("njh", "தொ");
    
    text = text.replace("jh", "தா");
    
    text = text.replace("jp", "தி");
    
    text = text.replace("jP", "தீ");
    
    text = text.replace("Jh", "தூ");
    
    text = text.replace("Jh", "தூ");
    
    text = text.replace("J}", "தூ");
    
    text = text.replace("J", "து");
    
    text = text.replace("nj", "தெ");
    
    text = text.replace("Nj", "தே");
    
    text = text.replace("ij", "தை");
    
    text = text.replace("j;", "த்");
    
    text = text.replace("j", "த");
    
    
    
    text = text.replace("nes", "நௌ");
    
    text = text.replace("Neh", "நோ");
    
    text = text.replace("neh", "நொ");
    
    text = text.replace("eh", "நா");
    
    text = text.replace("ep", "நி");
    
    text = text.replace("eP", "நீ");
    
    text = text.replace("E}", "நூ");
    
    text = text.replace("Eh", "நூ");
    
    text = text.replace("E", "நு");
    
    text = text.replace("ne", "நெ");
    
    text = text.replace("Ne", "நே");
    
    text = text.replace("ie", "நை");
    
    text = text.replace("e;", "ந்");
    
    text = text.replace("e", "ந");
    
    
    
    
    
    text = text.replace("nds", "னௌ");
    
    text = text.replace("Ndh", "னோ");
    
    text = text.replace("ndh", "னொ");
    
    text = text.replace("dh", "னா");
    
    text = text.replace("dp", "னி");
    
    text = text.replace("dP", "னீ");
    
    text = text.replace("D}", "னூ");
    
    
    
    text = text.replace("Dh", "னூ");
    
    text = text.replace("D", "னு");
    
    text = text.replace("nd", "னெ");
    
    text = text.replace("Nd", "னே");
    
    text = text.replace("id", "னை");
    
    text = text.replace("d;", "ன்");
    
    text = text.replace("d", "ன");
    
    
    
    text = text.replace("ngs", "பௌ");
    
    text = text.replace("Ngh", "போ");
    
    text = text.replace("ngh", "பொ");
    
    text = text.replace("gh", "பா");
    
    text = text.replace("gp", "பி");
    
    text = text.replace("gP", "பீ");
    
    
    
    
    
    text = text.replace("G", "பு");
    
    text = text.replace("ng", "பெ");
    
    text = text.replace("Ng", "பே");
    
    text = text.replace("ig", "பை");
    
    text = text.replace("g;", "ப்");
    
    text = text.replace("g", "ப");
    
    
    
    text = text.replace("nks", "மௌ");
    
    text = text.replace("Nkh", "மோ");
    
    text = text.replace("nkh", "மொ");
    
    text = text.replace("kh", "மா");
    
    text = text.replace("kp", "மி");
    
    text = text.replace("kP", "மீ");
    
    text = text.replace("K", "மு");
    
    text = text.replace("%", "மூ");
    
    text = text.replace("nk", "மெ");
    
    text = text.replace("Nk", "மே");
    
    text = text.replace("ik", "மை");
    
    text = text.replace("k;", "ம்");
    
    text = text.replace("k", "ம");
    
    
    
    
    
    text = text.replace("nas", "யௌ");
    
    text = text.replace("Nah", "யோ");
    
    text = text.replace("nah", "யொ");
    
    text = text.replace("ah", "யா");
    
    text = text.replace("ap", "யி");
    
    text = text.replace("aP", "யீ");
    
    text = text.replace("A", "யு");
    
    text = text.replace("A+", "யூ");
    
    text = text.replace("na", "யெ");
    
    text = text.replace("Na", "யே");
    
    text = text.replace("ia", "யை");
    
    text = text.replace("a;", "ய்");
    
    text = text.replace("a", "ய");
    
    
    
    text = text.replace("nus", "ரௌ");
    
    text = text.replace("Nuh", "ரோ");
    
    text = text.replace("nuh", "ரொ");
    
    text = text.replace("uh", "ரா");
    
    text = text.replace("up", "ரி");
    
    
    
    
    
    text = text.replace("U", "ரு");
    
    text = text.replace("&", "ரூ");
    
    text = text.replace("nu", "ரெ");
    
    text = text.replace("Nu", "ரே");
    
    text = text.replace("iu", "ரை");
    
    
    
    text = text.replace("u", "ர");
    
    
    
    text = text.replace("nys", "லௌ");
    
    text = text.replace("Nyh", "லோ");
    
    text = text.replace("nyh", "லொ");
    
    text = text.replace("yh", "லா");
    
    text = text.replace("yp", "லி");
    
    text = text.replace("yP", "லீ");
    
    text = text.replace("Yh", "லூ");
    
    text = text.replace("Y}", "லூ");
    
    text = text.replace("Y", "லு");
    
    text = text.replace("ny", "லெ");
    
    text = text.replace("Ny", "லே");
    
    text = text.replace("iy", "லை");
    
    text = text.replace("y;", "ல்");
    
    text = text.replace("y", "ல");
    
    
    
    text = text.replace("nss", "ளௌ");
    
    text = text.replace("Nsh", "ளோ");
    
    text = text.replace("nsh", "ளொ");
    
    text = text.replace("sh", "ளா");
    
    
    
    text = text.replace("sP", "ளீ");
    
    text = text.replace("Sh", "ளூ");
    
    text = text.replace("S", "ளு");
    
    text = text.replace("ns", "ளெ");
    
    text = text.replace("Ns", "ளே");
    
    text = text.replace("is", "ளை");
    
    text = text.replace("s;", "ள்");
    
    text = text.replace("s", "ள");
    
    
    
    
    
    text = text.replace("ntt", "வௌ");
    
    text = text.replace("Nth", "வோ");
    
    text = text.replace("nth", "வொ");
    
    text = text.replace("th", "வா");
    
    text = text.replace("tp", "வி");
    
    text = text.replace("tP", "வீ");
    
    
    
    
    
    
    
    
    
    text = text.replace("nt", "வெ");
    
    text = text.replace("Nt", "வே");
    
    text = text.replace("it", "வை");
    
    
    
    text = text.replace("t;", "வ்");
    
    text = text.replace("t", "வ");
    
    text = text.replace("noo", "ழௌ");
    
    text = text.replace("Noh", "ழோ");
    
    text = text.replace("noh", "ழொ");
    
    text = text.replace("oh", "ழா");
    
    text = text.replace("op", "ழி");
    
    text = text.replace("oP", "ழீ");
    
    text = text.replace("\*", "ழூ");
    
    text = text.replace("O", "ழு");
    
    text = text.replace("no", "ழெ");
    
    text = text.replace("No", "ழே");
    
    text = text.replace("io", "ழை");
    
    text = text.replace("o;", "ழ்");
    
    text = text.replace("o", "ழ");
    
    
    
    text = text.replace("nws", "றௌ");
    
    text = text.replace("Nwh", "றோ");
    
    text = text.replace("nwh", "றொ");
    
    text = text.replace("wh", "றா");
    
    text = text.replace("wp", "றி");
    
    text = text.replace("wP", "றீ");
    
    text = text.replace("Wh", "றூ");
    
    text = text.replace("W}", "றூ");
    
    
    
    text = text.replace("W", "று");
    
    text = text.replace("nw", "றெ");
    
    text = text.replace("Nw", "றே");
    
    text = text.replace("iw", "றை");
    
    text = text.replace("w;", "ற்");
    
    text = text.replace("w", "ற");
    
    
    
    text = text.replace("n``", "ஹௌ");
    
    text = text.replace("N`h", "ஹோ");
    
    text = text.replace("n`h", "ஹொ");
    
    text = text.replace("`h", "ஹா");
    
    text = text.replace("`p", "ஹி");
    
    text = text.replace("`P", "ஹீ");
    
    
    
    text = text.replace("n`", "ஹெ");
    
    text = text.replace("N`", "ஹே");
    
    text = text.replace("i`", "ஹை");
    
    text = text.replace("`;", "ஹ்");
    
    text = text.replace("`", "ஹ");
    
    
    
    text = text.replace("n\\s", "ஷௌ");
    
    text = text.replace("N\\h", "ஷோ");
    
    text = text.replace("n\\h", "ஷொ");
    
    text = text.replace("\\h", "ஷா");
    
    text = text.replace("\\p", "ஷி");
    
    text = text.replace("\\P", "ஷீ");
    
    
    
    text = text.replace("n\\", "ஷெ");
    
    text = text.replace("N\\", "ஷே");
    
    text = text.replace("i\\", "ஷை");
    
    text = text.replace("\\;", "ஷ்");
    
    text = text.replace("\\", "ஷ");
    
    
    
    
    
    text = text.replace("n]s", "ஸௌ");
    
    text = text.replace("N]h", "ஸோ");
    
    text = text.replace("n]h", "ஸொ");
    
    text = text.replace("]h", "ஸா");
    
    text = text.replace("]p", "ஸி");
    
    text = text.replace("]P", "ஸீ");
    
    
    
    text = text.replace("n]", "ஸெ");
    
    text = text.replace("N]", "ஸே");
    
    text = text.replace("i]", "ஸை");
    
    text = text.replace("];", "ஸ்");
    
    text = text.replace("]", "ஸ");
    
    
    
    
    
    text = text.replace(">", "ää");
    
    text = text.replace("m", "அ");
    
    text = text.replace("M", "ஆ");
    
    text = text.replace("<", "ஈ");
    
    text = text.replace("c", "உ");
    
    text = text.replace("C", "ஊ");
    
    text = text.replace("v", "எ");
    
    text = text.replace("V", "ஏ");
    
    text = text.replace("I", "ஐ");
    
    text = text.replace("x", "ஒ")
    
    text = text.replace("X", "ஓ");
    
    text = text.replace("xs", "ஔ");
    
    
    
    
    
    
    
    text = text.replace("\/", "ஃ");
    
    
    
    
    
    text = text.replace(",", "இ");
    
    
    
    text = text.replace("=", "ஸ்ரீ");
    
    
    
    text = text.replace(">", ",");
    
    
    
    text = text.replace("T", "வு");
    
    
    
    text = text.replace("ää", ",");
    
    text = text.replace("வு+", "வூ");
    
    text = text.replace("பு+", "பூ");
    
    text = text.replace("யு+", "யூ");
    
    text = text.replace("சு+", "சூ");
    
    
    
    text = text.replace("+", "ூ");
    
    text = text.replace("\@", ";");
    
    return text;

def writeHindi(in_txt):
    array_one = ["ñ", "Q+Z", "sas", "aa", ")Z", "ZZ", "‘", "’", "“", "”",
                 "å", "ƒ", "„", "…", "†", "‡", "ˆ", "‰", "Š", "‹",
                 "¶+", "d+", "[+k", "[+", "x+", "T+", "t+", "M+", "<+", "Q+",
                 ";+", "j+", "u+", "Ùk", "Ù", "ä", "–", "—", "é", "™",
                 "=kk", "f=k", "à", "á", "â", "ã", "ºz", "º", "í", "{k",
                 "{", "=", "«", "Nî", "Vî", "Bî", "Mî", "<î", "|", "K",
                 "}", "J", "Vª", "Mª", "<ªª", "Nª", "Ø", "Ý", "nzZ", "æ",
                 "ç", "Á", "xz", "#", ":", "v‚", "vks", "vkS", "vk", "v",
                 "b±", "Ã", "bZ", "b", "m", "Å", ",s", ",", "_", "ô",
                 "d", "Dk", "D", "[k", "[", "x", "Xk", "X", "Ä", "?k",
                 "?", "³", "pkS", "p", "Pk", "P", "N", "t", "Tk", "T",
                 ">", "÷", "¥", "ê", "ë", "V", "B", "ì", "ï", "M+",
                 "<+", "M", "<", ".k", ".", "r", "Rk", "R", "Fk", "F",
                 ")", "n", "/k", "èk", "/", "Ë", "è", "u", "Uk", "U",
                 "i", "Ik", "I", "Q", "¶", "c", "Ck", "C", "Hk", "H",
                 "e", "Ek", "E", ";", "¸", "j", "y", "Yk", "Y", "G",
                 "o", "Ok", "O", "'k", "'", "\"k", "\"", "l", "Lk", "L",
                 "g", "È", "z", "Ì", "Í", "Î", "Ï", "Ñ", "Ò", "Ó",
                 "Ô", "Ö", "Ø", "Ù", "Ük", "Ü", "‚", "ks", "kS", "k",
                 "h", "q", "w", "`", "s", "S", "a", "¡", "%", "W",
                 "•", "·", "∙", "·", "~j", "~", "\\", "+", " ः", "^",
                 "*", "Þ", "ß", "(", "¼", "½", "¿", "À", "¾", "A",
                 "-", "&", "&", "Œ", "]", "~ ", "@"]
    
    array_two = ["॰", "QZ+", "sa", "a", "र्द्ध", "Z", "\"", "\"", "'", "'",
                 "०", "१", "२", "३", "४", "५", "६", "७", "८", "९",
                 "फ़्", "क़", "ख़", "ख़्", "ग़", "ज़्", "ज़", "ड़", "ढ़", "फ़",
                 "य़", "ऱ", "ऩ", "त्त", "त्त्", "क्त", "दृ", "कृ", "न्न", "न्न्",
                 "=k", "f=", "ह्न", "ह्य", "हृ", "ह्म", "ह्र", "ह्", "द्द", "क्ष",
                 "क्ष्", "त्र", "त्र्", "छ्य", "ट्य", "ठ्य", "ड्य", "ढ्य", "द्य", "ज्ञ",
                 "द्व", "श्र", "ट्र", "ड्र", "ढ्र", "छ्र", "क्र", "फ्र", "र्द्र", "द्र",
                 "प्र", "प्र", "ग्र", "रु", "रू", "ऑ", "ओ", "औ", "आ", "अ",
                 "ईं", "ई", "ई", "इ", "उ", "ऊ", "ऐ", "ए", "ऋ", "क्क",
                 "क", "क", "क्", "ख", "ख्", "ग", "ग", "ग्", "घ", "घ",
                 "घ्", "ङ", "चै", "च", "च", "च्", "छ", "ज", "ज", "ज्",
                 "झ", "झ्", "ञ", "ट्ट", "ट्ठ", "ट", "ठ", "ड्ड", "ड्ढ", "ड़",
                 "ढ़", "ड", "ढ", "ण", "ण्", "त", "त", "त्", "थ", "थ्",
                 "द्ध", "द", "ध", "ध", "ध्", "ध्", "ध्", "न", "न", "न्",
                 "प", "प", "प्", "फ", "फ्", "ब", "ब", "ब्", "भ", "भ्",
                 "म", "म", "म्", "य", "य्", "र", "ल", "ल", "ल्", "ळ",
                 "व", "व", "व्", "श", "श्", "ष", "ष्", "स", "स", "स्",
                 "ह", "ीं", "्र", "द्द", "ट्ट", "ट्ठ", "ड्ड", "कृ", "भ", "्य",
                 "ड्ढ", "झ्", "क्र", "त्त्", "श", "श्", "ॉ", "ो", "ौ", "ा",
                 "ी", "ु", "ू", "ृ", "े", "ै", "ं", "ँ", "ः", "ॅ",
                 "ऽ", "ऽ", "ऽ", "ऽ", "्र", "्", "?", "़", ":", "‘",
                 "’", "“", "”", ";", "(", ")", "{", "}", "=", "।",
                 ".", "-", "µ", "॰", ", ", "् ", "/"]
    
    
    for counter in range(len(array_one)):
        in_txt = in_txt.replace(array_one[counter], array_two[counter])
    
    #Some additional replacements
    in_txt = in_txt.replace( '±' , "Zं" )
    in_txt = in_txt.replace( 'Æ' , "र्f" )
    
    #**********************************************************************************
    # Glyp2: Æ
    # code for replacing "f" with "ि" and correcting its position too. (moving it one position forward)
    #**********************************************************************************
    
    position_of_i = 0
    position_of_i = in_txt.find("f")
    
    
    
    while position_of_i != -1:
            
        charecter_next_to_i = in_txt[position_of_i + 1]
        charecter_to_be_replaced = "f" + charecter_next_to_i
        in_txt = in_txt.replace( charecter_to_be_replaced , charecter_next_to_i + "ि", 1) #replace only one char at a time
        position_of_i = in_txt.find( 'f' , position_of_i + 1 ) # search for i ahead of the current position.
    
    #**********************************************************************************
    # Glyph3 & Glyph4: Ç  É
    # code for replacing "fa" with "िं"  and correcting its position too.(moving it two positions forward)
    #**********************************************************************************
    
    in_txt = in_txt.replace( 'Ç' , "fa" )
    in_txt = in_txt.replace( 'É' , "र्fa" )
    
    position_of_i = 0
    position_of_i = in_txt.find("fa")
    while position_of_i != -1:
        charecter_next_to_ip2 = in_txt[position_of_i + 2]
        charecter_to_be_replaced = "fa" + charecter_next_to_ip2
        in_txt = in_txt.replace(charecter_to_be_replaced , charecter_next_to_ip2 + "िं")
        position_of_i = in_txt.find( "fa" , position_of_i + 2 ) #search for i ahead of the current position.
    
    print(in_txt)
    
    #**********************************************************************************
    # Glyph5: Ê
    # code for replacing "h" with "ी"  and correcting its position too.(moving it one positions forward)
    #**********************************************************************************
    
    in_txt = in_txt.replace( 'Ê' , "ीZ" ) # at some places  Ê  is  used eg  in "किंकर".
    
    position_of_wrong_ee = in_txt.find("ि्")
    
    while position_of_wrong_ee != -1:
        consonent_next_to_wrong_ee = in_txt[position_of_wrong_ee + 2]
        charecter_to_be_replaced = "ि्" + consonent_next_to_wrong_ee
        modified_substring = in_txt.replace( charecter_to_be_replaced , "्" + consonent_next_to_wrong_ee + "ि")
        position_of_wrong_ee = in_txt.find( "ि्" , position_of_wrong_ee + 2 ) # search for 'wrong ee' ahead of the current position.
    
    print(in_txt)
    
    #Ok till here...
    
    
    
    #Need to check for replacement of "Z" character_to_be_replaced
    
    position_of_R = 0
    position_of_R = in_txt.find( "Z" )
    print(position_of_R)
    
    
    
    # Eliminating reph "Z" and putting 'half - r' at proper position for this.
    set_of_matras = "अ आ इ ई उ ऊ ए ऐ ओ औ ा ि ी ु ू ृ े ै ो ौ ं : ँ ॅ"
    
    position_of_R = 0
    position_of_R = in_txt.find( "Z" )
    
    while position_of_R > 0:
     probable_position_of_half_r = position_of_R - 1 ;
     charecter_at_probable_position_of_half_r = in_txt[probable_position_of_half_r]
     #print('charecter_at_probable_position_of_half_r', charecter_at_probable_position_of_half_r)
     # trying to find non-maatra position left to current O (ie, half -r).
    
     while set_of_matras.find(charecter_at_probable_position_of_half_r) != -1:
         #print("here..")
         probable_position_of_half_r = probable_position_of_half_r - 1
         charecter_at_probable_position_of_half_r = in_txt[probable_position_of_half_r]
         #print("here..",charecter_at_probable_position_of_half_r)
    
     character_to_be_replaced = in_txt[ probable_position_of_half_r : probable_position_of_half_r + ( position_of_R - probable_position_of_half_r + 1)]
     #print("After substring:",character_to_be_replaced)
     #charecter_to_be_replaced = in_txt.substr ( probable_position_of_half_r , ( position_of_R - probable_position_of_half_r ) )
     new_replacement_string = "र्" + charecter_to_be_replaced
     #print("new replacement string:र् + ", new_replacement_string)
     charecter_to_be_replaced = charecter_to_be_replaced + "Z"
     #print(charecter_to_be_replaced)
     modified_substring = in_txt.replace( charecter_to_be_replaced , new_replacement_string)
     position_of_R = in_txt.find("Z", position_of_R + 1)
     return in_txt

def convert_tamil_utf8_newKannanText(fin, fout):
    for line in fin:
        fout.write (writeTamil(line))

def convert_hindi_utf8_krutidev(fin, fout):
    for line in fin:
        fout.write (writeHindi(line))

def print_usage(binary_name):
   print 'Error Usage: ', binary_name, '-i <inputfile> -o <outputfile> -l <french/hindi/tamil>'
   sys.exit(2)

def main(binary_name, argv):
   infile = ''
   outfile = ''
   language = ''
   if len(argv) == 0:
      print_usage(binary_name)
      
   try:
      opts, args = getopt.getopt(argv,"hi:o:l:",["help", "ifile=","ofile=", "language"])
   except getopt.GetoptError:
      print_usage(binary_name)
   for opt, arg in opts:
      if opt in ( "-h", "--help"):
         print_usage(binary_name)
      elif opt in ("-i", "--ifile"):
         infile = arg
      elif opt in ("-o", "--ofile"):
         outfile = arg
      elif opt in ("-l", "--language"):
         language = arg
   print 'Input file is ', infile
   print 'Output file is ', outfile
   print 'Language is ', language

   if (infile == '' or outfile == '' or language == ''):
	print_usage(binary_name)

   try:
      fin = open(infile, 'r')
   except:
      str= "Cannot open input file " + infile + "\n"
      sys.stderr.write(str)
      exit(1)
   
   try:
      fout = open(outfile, 'w')
   except:
      str= "Cannot open output file " + outfile + "\n"
      sys.stderr.write(str)
      exit(1)
         
   if (language == "tamil"):
      convert_tamil_utf8_newKannanText(fin, fout)
   elif (language == "hindi"):
      convert_hindi_utf8_krutidev(fin, fout)
   
   fin.close()
   fout.close()
       
#ascii_tamil="ekJ rf[ khh;f;fj;jpd; gapw;rpapDila Kf;fpaj;Jtj;ijg;gw;wp (,ijtpl) vd;djhd; mjpfkhfr; nrhy;yptplf;$Lk;?  NkYk; ekJ mg;gpahrpfs; vspjpy; fpufpj;Jf; nfhs;sf;$ba (sensitise) Kiwapy; vd;djhd; nra;Jtpl KbAk;?  mjpy;jhd; mjDila njspthd vspikfs; cs;sd my;yth?  gapw;rpNa> kpf mUikahd gyhgyd;fis cw;gj;jp nra;Jjuf; $bajhf ,Uf;fpwJ.  gapw;rpahdJ xU #l;Rkkhd [Ptid md;G kw;Wk; mikjpAk; cs;s RoYf;Fs; (spirals) mioj;Jr; nry;fpwJ.  mjpYk; Kd;Ndw;wj;ij Nehf;fpr; nrd;Wnfhz;bUf;Fk;  mg;gpahrp rNfhju> rNfhjhpfspy; mNefk; NgiuAk; <LghLf; nfhs;sr; nra;fpwJ> <Lglr;nra;fpwJ.  xU gpwtpapypUe;J mLj;j gpwtpf;Fk;$l nja;tj;Jld; xUq;fpiz tjw;fhd Njit vOk;gpf;nfhz;Nl (cjakhfpf; nfhz;Nl) ,Uf;fpwJ.  xU KOikahd miog;ghdJ jg;gpf;fglNt nra;ahJ mjhtJ gyd;juhky; jg;gptplhJ.  mth;fSf;Fs; cs;shh;e;j epiyapy;> Md;kPfj;jpd; cz;ikj; Njitia czh;j;jpa gpd;Gk; czh;j;jpa gpw;ghLk;> mNeftpjkhd gpwtpfs; khw;wg;gl;Ls;sd.  (jpahdj;jpy;) cs;shh;e;J nry;Ytjw;Fj; jw;fhyj;jpy; cs;s cyfkhdJ> (cyfj;jpYs;s fth;r;rpahdJ) kdpj ,yf;if vspjpy; tpl;LtpLtJ fpilahJ.  mth;fSila kdkhdJ ,e;j nghUl;fshyhd cyfj;jpd; ,af;fj;jpy; fth;e;J ,Of;fg;gl;Ls;sd.  mwpT epiwe;j kf;fNsh nfhQ;r Neuj;ij Md;kPfj;Jf;fhf xJf;fp itj;J>  Md;kPfj;jpd; mj;jpahtrpakhd mbg;gil gapw;rpfis Nkw;nfhz;L tUfpwhh;fs;.  mJTk; mth;fspd; nrhe;j jdpg;gl;l topfspy;jhd; nra;JtUfpwhh;fs;.  mjd; fhuzkhf> mth;fs; tho;e;JtUk; vjph;kiw> mitfspd; mjph;tpypUe;J fle;Jte;J> jdpj;jpUe;J> njhlh;e;J tho;e;J tUfpd;wdh;.  fle;j fhyj;jpy; rhJf;fs; ghJfhf;fg;gl;l ,lq;fSf;F xJq;fp (gpd;thq;fp) ,Ue;jhh;fs;.  mjhtJ Vfhe;jkhf xJq;fpapUe;J thoe;J te;jhh;fs;.  Mdhy; ek;kpy; Mh;tkpf;f tplh Kaw;rpAila mg;gpahrpfs;> jpdrhp jpahdj;jpw;F jdpahf Neuk; xJf;Ftjpy; rkhspj;J (Manage) eph;tfpj;J tUfpwhh;fs;.  ek;Kld; tho;e;JtUk; kh];lUld; xUq;fpizj;J ,Ug;gjw;Fk>; Neuj;ij xJf;fp rkhspj;J tUfpwhh;fs;.  mJTk; jq;fspd; ,jaq;fspd; %ykhf> cj;Ntfj;Jld; mtUld; (Mtpapy;) xUq;fpize;jpUf;fTk; nra;fpwhh;fs;.  nja;tPf rf;jpia mUl;gha;r;Rjy; vd;gJ cz;ikahfNt ,Ue;J tUfpwJ.  mjDld; njhlh;G nfhs;sNtz;baJ xd;Wjhd; Njitahf cs;sJ.  mjpYk;> nja;tPfj;Jf;Fs; ruzhfjp mile;J> mikjpahFk; cz;ikahd jUzj;jpw;Fs;> %o;fptplTk; (ek;ik) tpl;Ltpl Ntz;Lk;.  rhpahd tha;g;Gs;s Neuq;fspy;> (nja;t md;gpDila) mUshdJ> jd;Dila nrhe;j topfspy;> Ntiynra;J nfhz;Lk; ,Uf;fpwJ.  mjpYk; mts; my;yJ mtDila cs;shh;e;j miog;Gf;Fj; jFe;jgb xt;nthUtUf;Fk; chpa mD$yk; jia my;yJ ed;ikfshf nra;af; $bajhfTk; ,Uf;fpwJ. me;jtpjkhd epiyikapy; ,e;j cs;shh;e;j miog;G xd;Nw kpf Kf;fpak; tha;e;jjhfTk; ,Uf;fpd;wJ.  vd;d Ntz;LkhdhYk; epfof;$Lk;.  mtutUila jiytpjpahdJ mJthfNt ntspg;gLk; gl;rj;jpy;> xUtUila tho;f;ifiaNa> KOtJkhf khw;wk; ngw;Wf;nfhz;Ljhd; ,Ue;J tUfpd;wJ.  midtUf;fk; MrPh;thjq;fs; toq;FfpNwhk;.  --ghg+[p kfhuh[;"
   #u=unicode(ascii, "utf-8")
   #print "Orig String:", ascii
   

if __name__ == "__main__":
   main(sys.argv[0], sys.argv[1:])
