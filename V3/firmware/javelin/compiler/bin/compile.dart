import 'dart:io';
import 'package:javelin_steno_script/javelin_steno_script.dart';
void main(List<String> args) {
  final result = ScriptCompileResult.buttonScript(
    script: File(args[0]).readAsStringSync(), scriptHeader: '',
    buttonCount: 31, analogInputCount: 0, encoderCount: 0, pointerCount: 0,
    maximumByteCodeSize: 0x7f00, byteCodeVersion: 4);
  if (!result.success || result.data == null) throw Exception(result.message);
  File(args[1]).writeAsBytesSync(result.data!);
  print('Compiled 31-button JSS4 bytecode: ${result.data!.length} bytes');
}
