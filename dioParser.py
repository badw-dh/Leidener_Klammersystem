#!/usr/bin/env python3

#######################################################################
#
# SYMBOLS SECTION - Can be edited. Changes will be preserved.
#
#######################################################################


import collections
from functools import partial
import os
import sys
from typing import Tuple, List, Union, Any, Optional, Callable, cast

try:
    import regex as re
except ImportError:
    import re

try:
    scriptdir = os.path.dirname(os.path.realpath(__file__))
except NameError:
    scriptdir = ''
if scriptdir and scriptdir not in sys.path: sys.path.append(scriptdir)

try:
    from DHParser import versionnumber
except (ImportError, ModuleNotFoundError):
    i = scriptdir.rfind("/DHParser/")
    if i >= 0:
        dhparserdir = scriptdir[:i + 10]  # 10 = len("/DHParser/")
        if dhparserdir not in sys.path:  sys.path.insert(0, dhparserdir)

from DHParser.compile import Compiler, compile_source, Junction, full_compile
from DHParser.configuration import set_config_value, add_config_values, get_config_value, \
    access_thread_locals, access_presets, finalize_presets, set_preset_value, \
    get_preset_value, NEVER_MATCH_PATTERN
from DHParser import dsl
from DHParser.dsl import recompile_grammar, never_cancel
from DHParser.ebnf import grammar_changed
from DHParser.error import ErrorCode, Error, canonical_error_strings, has_errors, NOTICE, \
    WARNING, ERROR, FATAL
from DHParser.log import start_logging, suspend_logging, resume_logging
from DHParser.nodetree import Node, WHITESPACE_PTYPE, TOKEN_PTYPE, RootNode, Path, ZOMBIE_TAG
from DHParser.parse import Grammar, PreprocessorToken, Whitespace, Drop, DropFrom, AnyChar, Parser, \
    Lookbehind, Lookahead, Alternative, Pop, Text, Synonym, Counted, Interleave, INFINITE, ERR, \
    Option, NegativeLookbehind, OneOrMore, RegExp, SmartRE, Retrieve, Series, Capture, TreeReduction, \
    ZeroOrMore, Forward, NegativeLookahead, Required, CombinedParser, Custom, IgnoreCase, \
    LateBindingUnary, mixin_comment, last_value, matching_bracket, optional_last_value, \
    PARSER_PLACEHOLDER, UninitializedError
from DHParser.pipeline import end_points, full_pipeline, create_parser_junction, \
    create_preprocess_junction, create_junction, PseudoJunction
from DHParser.preprocess import nil_preprocessor, PreprocessorFunc, PreprocessorResult, \
    gen_find_include_func, preprocess_includes, make_preprocessor, chain_preprocessors
from DHParser.stringview import StringView
from DHParser.toolkit import is_filename, load_if_file, cpu_count, RX_NEVER_MATCH, \
    ThreadLocalSingletonFactory, expand_table
from DHParser.trace import set_tracer, resume_notices_on, trace_history
from DHParser.transform import is_empty, remove_if, TransformationDict, TransformerFunc, \
    transformation_factory, remove_children_if, move_fringes, normalize_whitespace, \
    is_anonymous, name_matches, reduce_single_child, replace_by_single_child, replace_or_reduce, \
    remove_whitespace, replace_by_children, remove_empty, remove_tokens, flatten, all_of, \
    any_of, transformer, merge_adjacent, collapse, collapse_children_if, transform_result, \
    remove_children, remove_content, remove_brackets, change_name, remove_anonymous_tokens, \
    keep_children, is_one_of, not_one_of, content_matches, apply_if, peek, \
    remove_anonymous_empty, keep_nodes, traverse_locally, strip, lstrip, rstrip, \
    replace_content_with, forbid, assert_content, remove_infix_operator, add_error, error_on, \
    left_associative, lean_left, node_maker, has_descendant, neg, has_ancestor, insert, \
    positions_of, replace_child_names, add_attributes, delimit_children, merge_connected, \
    has_attr, has_parent, has_children, has_child, apply_unless, apply_ifelse, traverse
from DHParser import parse as parse_namespace__

import DHParser.versionnumber
if DHParser.versionnumber.__version_info__ < (1, 8, 2):
    print(f'DHParser version {DHParser.versionnumber.__version__} is lower than the DHParser '
          f'version 1.8.2, {os.path.basename(__file__)} has first been generated with. '
          f'Please install a more recent version of DHParser to avoid unexpected errors!')


#######################################################################
#
# PREPROCESSOR SECTION - Can be edited. Changes will be preserved.
#
#######################################################################



# To capture includes, replace the NEVER_MATCH_PATTERN
# by a pattern with group "name" here, e.g. r'\input{(?P<name>.*)}'
RE_INCLUDE = NEVER_MATCH_PATTERN
RE_COMMENT = NEVER_MATCH_PATTERN  # THIS MUST ALWAYS BE THE SAME AS dioGrammar.COMMENT__ !!!


def dioTokenizer(original_text) -> Tuple[str, List[Error]]:
    # Here, a function body can be filled in that adds preprocessor tokens
    # to the source code and returns the modified source.
    return original_text, []

preprocessing: PseudoJunction = create_preprocess_junction(
    dioTokenizer, RE_INCLUDE, RE_COMMENT)


#######################################################################
#
# PARSER SECTION - Don't edit! CHANGES WILL BE OVERWRITTEN!
#
#######################################################################

class dioGrammar(Grammar):
    r"""Parser for a dio source file.
    """
    brackets = Forward()
    inline = Forward()
    tags = Forward()
    source_hash__ = "f8991c6886e21adcc03dda8cc835d5ed"
    early_tree_reduction__ = CombinedParser.MERGE_LEAVES
    disposable__ = re.compile('(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:(?:inscription$))|(?:inline$))|(?:tags$))|(?:app$))|(?:insec_combined_plain$))|(?:insec_combined_extended$))|(?:insec_precomposed$))|(?:insec_binder$))|(?:insec_separator$))|(?:letters_sequence$))|(?:letters_range$))|(?:letters_plain$))|(?:letters_extended$))|(?:letters_diacrytic$))|(?:letters_cross$))|(?:letters_apostrophe$))|(?:binder_equal$))|(?:binder_hyphen$))|(?:separator$))|(?:brackets$))|(?:lost$))|(?:unknown$))|(?:known$))|(?:prettyspace$))|(?:EOF$)')
    static_analysis_pending__ = []  # type: List[bool]
    parser_initialization__ = ["upon instantiation"]
    COMMENT__ = r''
    comment_rx__ = RX_NEVER_MATCH
    WHITESPACE__ = r' *'
    WSP_RE__ = mixin_comment(whitespace=WHITESPACE__, comment=COMMENT__)
    wsp__ = Whitespace(WSP_RE__)
    dwsp__ = Drop(Whitespace(WSP_RE__))
    EOF = Drop(NegativeLookahead(RegExp('.')))
    prettyspace = Drop(RegExp('[\\r\\n ]*'))
    sep_word_dot = Series(dwsp__, Text("·"), dwsp__)
    known = OneOrMore(Text("."))
    unknown = Alternative(Drop(Text("---")), Drop(Text("--")), Drop(Text("–––")), Drop(Text("- - -")), Drop(Text("– – –")), Drop(Text("–\u202f–\u202f–")))
    lost = Alternative(unknown, known)
    deletion_nested = Synonym(lost)
    add = Series(Alternative(Drop(Text("&lt;")), Drop(Text("⟨"))), OneOrMore(Alternative(tags, deletion_nested, inline, brackets)), Alternative(Drop(Text("&gt;")), Drop(Text("⟩"))))
    cpl = Series(Drop(Text("[")), OneOrMore(Alternative(tags, deletion_nested, inline, brackets)), Drop(Text("]")))
    deletion = Series(Drop(Text("[")), lost, Drop(Text("]")))
    abr = Series(Drop(Text("(")), OneOrMore(inline), Drop(Text(")")))
    b = Series(prettyspace, Drop(Text("<b>")), RegExp('[^<]+'), Drop(Text("</b>")), prettyspace)
    sep_line = Series(dwsp__, Text("/"), dwsp__)
    sep_field = Series(dwsp__, Text("//"), dwsp__)
    z = Alternative(sep_field, sep_line)
    sep_word_equal = RegExp('(?<!\\s)=(?!\\s)')
    sep_word_comma = Series(dwsp__, Text(","), dwsp__)
    sep_word_colon = Series(dwsp__, Text(":"), dwsp__)
    sep_word_period = Series(dwsp__, Text("."), dwsp__)
    wtr = Alternative(sep_word_dot, sep_word_period, sep_word_comma, sep_word_colon, sep_word_equal)
    separator = Alternative(z, wtr)
    space = Series(RegExp('\\s'), dwsp__, NegativeLookahead(separator))
    binder_hyphen = RegExp('(?<!-)-(?!-)')
    binder_equal = Text("=")
    binder = Alternative(binder_equal, binder_hyphen)
    terminator = RegExp('(?<!\\s)[\\.:,;]')
    letters_apostrophe = Text("\'")
    letters_cross = RegExp('[+†]')
    letters_diacrytic = OneOrMore(RegExp('[A-Za-z]̈(?!\\u0323)'))
    letters_extended = OneOrMore(RegExp('[àèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÃÑÕäëïöüÿÄËÏÖÜŸçÇßØøÅåÆæœ](?!\\u0323)'))
    letters_plain = OneOrMore(RegExp('[A-Za-z0-9](?!\\u0323)'))
    letters_sequence = Alternative(letters_plain, letters_extended, letters_diacrytic, letters_cross, letters_apostrophe)
    letters_range = Series(letters_sequence, Text("-"), letters_sequence)
    letters = Alternative(letters_range, letters_sequence)
    insec_separator = Series(wtr, RegExp(' ?(\\u0323)'), dwsp__)
    insec_binder = Series(binder, RegExp('\\u0323'))
    insec_precomposed = RegExp('[ẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓ]')
    insec_combined_extended = RegExp('[àèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÃÑÕäëïöüÿÄËÏÖÜŸçÇßØøÅåÆæœ]\\u0323')
    insec_combined_plain = RegExp('[a-zA-Z0-9]\\u0323')
    insec = Alternative(insec_combined_plain, insec_combined_extended, insec_precomposed, insec_binder, insec_separator)
    nl = Alternative(Drop(Text("<nl></nl>")), Drop(Text("<nl/>")))
    sub = Series(Drop(Text("<sub>")), letters, Option(space), Drop(Text("</sub>")))
    sup = Series(Drop(Text("<sup>")), letters, Option(space), Drop(Text("</sup>")))
    chr = Series(Drop(Text("<chr>")), letters, Option(space), Drop(Text("</chr>")))
    em = Series(Drop(Text("<em>")), letters, Option(space), Drop(Text("</em>")))
    all = Series(Drop(Text("<lig>")), OneOrMore(Alternative(letters, brackets, space)), Drop(Text("</lig>")))
    app_nr = RegExp('[^<]*')
    app_id = RegExp('[^>]*')
    appnum = Series(Drop(Text("<appnum id=")), app_id, Drop(Text(">")), app_nr, Drop(Text("</appnum>")))
    appalpha = Series(Drop(Text("<appalpha id=")), app_id, Drop(Text(">")), app_nr, Drop(Text("</appalpha>")))
    app = Alternative(appalpha, appnum)
    snr = Series(Drop(Text("<snr>")), RegExp('[A-Z0-9]+'), Option(Text(".")), Option(letters_cross), prettyspace, Drop(Text("</snr>")), prettyspace)
    snt = Series(Drop(Text("<snt>")), Alternative(b, RegExp('[^<]+')), Drop(Text("</snt>")), prettyspace)
    inscription = OneOrMore(Alternative(inline, brackets))
    entry = Series(Drop(Text("<entry>")), inscription, Drop(Text("</entry>")), prettyspace, mandatory=1)
    cell = Series(Drop(Text("<cell>")), prettyspace, OneOrMore(entry), Drop(Text("</cell>")), prettyspace)
    row = Series(Drop(Text("<row>")), prettyspace, OneOrMore(cell), Drop(Text("</row>")), prettyspace)
    table = Series(Drop(Text("<table>")), prettyspace, OneOrMore(row), Drop(Text("</table>")), prettyspace)
    cnt = Series(Drop(Text("<cnt>")), RegExp('[0-9]+'), Drop(Text("</cnt>")))
    lin = Series(Drop(Text("<lin>")), Option(cnt), inscription, Drop(Text("</lin>")), prettyspace, mandatory=2)
    lno = Series(Drop(Text("<lno>")), Option(cnt), inscription, Drop(Text("</lno>")), prettyspace, mandatory=2)
    par = Series(Drop(Text("<par>")), prettyspace, OneOrMore(Alternative(lno, lin, table)), Drop(Text("</par>")), prettyspace)
    sec = Series(Drop(Text("<sec>")), prettyspace, ZeroOrMore(Alternative(snt, snr)), ZeroOrMore(par), Drop(Text("</sec>")), prettyspace)
    brackets.set(Alternative(abr, deletion, cpl, add))
    tags.set(Alternative(app, all, em, chr, sup, sub, nl))
    inline.set(Alternative(tags, insec, letters, terminator, binder, separator, space))
    sco = Series(prettyspace, Drop(Text("<sco>")), prettyspace, OneOrMore(sec), Drop(Text("</sco>")), prettyspace, EOF, mandatory=6)
    root__ = sco
    
parsing: PseudoJunction = create_parser_junction(dioGrammar)
get_grammar = parsing.factory # for backwards compatibility, only


#######################################################################
#
# AST SECTION - Can be edited. Changes will be preserved.
#
#######################################################################


def count_characters(path: Path):
    node = path[-1]
    assert not node.children
    node.attr['num_sign'] = len(node.content)
    node.result = ''

def move_app_id_to_attr(path: Path):
    node = path[-1]

    assert len(node.children) == 2
    node.attr['id'] = node.children[0].content.strip('"')
    node.result = node.children[1].content

def remove_dot_below(path: Path):
    currentNode = path[-1]

    nodes = list(currentNode.children) + [currentNode]

    for node in nodes:
        plain = node.content
        if plain != "":

            # Translate precomposed characters
            translate_from = "ẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓ"
            translate_to   = "ABDEHIKLMNORSTUVWYZabdehiklmnorstuvwyz"
            plain = plain.translate(str.maketrans(translate_from, translate_to))

            # Remove combined dot
            plain = plain.replace(u"\u0323","")

            node.result = plain


def move_content_to_attr(path: Path):
    node = path[-1]
    assert not node.children
    node.attr['type'] = node.name.replace('sep_word_','').replace('sep_','')
    node.attr['rend'] = node.content
    node.result = ''

dio_AST_transformation_table = {
    # AST Transformations for the dio-grammar
    # "<": [],  # called for each node before calling its specific rules
    # "*": [],  # fallback for nodes that do not appear in this table
    # ">": [],   # called for each node after calling its specific rules
    "z" : [replace_by_single_child, move_content_to_attr, change_name("z")],
    "wtr" : [replace_by_single_child, move_content_to_attr, change_name("wtr")],
    "deletion" : [change_name("del"), replace_by_single_child, count_characters],
    "deletion_nested":  [change_name("del"), replace_by_single_child, count_characters],
    "appalpha" : [move_app_id_to_attr],
    "appnum" : [move_app_id_to_attr],
    "insec" : [remove_dot_below]
}


# DEPRECATED, because it requires pickling the transformation-table, which rules out lambdas!
# ASTTransformation: Junction = create_junction(
#     dio_AST_transformation_table, "CST", "AST", "transtable")

def dioTransformer() -> TransformerFunc:
    return partial(transformer, transformation_table=dio_AST_transformation_table.copy(),
                   src_stage='CST', dst_stage='AST')

ASTTransformation: Junction = Junction(
    'CST', ThreadLocalSingletonFactory(dioTransformer), 'AST')


#######################################################################
#
# COMPILER SECTION - Can be edited. Changes will be preserved.
#
#######################################################################

class dioCompiler(Compiler):
    """Compiler for the abstract-syntax-tree of a 
        dio source file.
    """

    def __init__(self):
        super(dioCompiler, self).__init__()
        self.forbid_returning_None = True  # set to False if any compilation-method is allowed to return None

    def reset(self):
        super().reset()
        # initialize your variables here, not in the constructor!

    def prepare(self, root: RootNode) -> None:
        assert root.stage == "AST", f"Source stage `AST` expected, `but `{root.stage}` found."
        root.stage = "dio"
    def finalize(self, result: Any) -> Any:
        return result

    def on_inscription(self, node):
        return self.fallback_compiler(node)

    # def on_inline(self, node):
    #     return node

    # def on_tags(self, node):
    #     return node

    # def on_apptag(self, node):
    #     return node

    # def on_tag(self, node):
    #     return node

    # def on_letters(self, node):
    #     return node

    # def on_phrases(self, node):
    #     return node

    # def on_partial(self, node):
    #     return node

    # def on_unreadable(self, node):
    #     return node

    # def on_space(self, node):
    #     return node

    # def on_separator(self, node):
    #     return node

    # def on_footnote(self, node):
    #     return node

    # def on_special(self, node):
    #     return node

    # def on_rasure(self, node):
    #     return node

    # def on_vacat(self, node):
    #     return node

    # def on_missing(self, node):
    #     return node

    # def on_restored(self, node):
    #     return node

    # def on_omission(self, node):
    #     return node

    # def on_litura(self, node):
    #     return node

    # def on_correct(self, node):
    #     return node

    # def on_false(self, node):
    #     return node

    # def on_redundancy(self, node):
    #     return node

    # def on_letter(self, node):
    #     return node

    # def on_unknown(self, node):
    #     return node

    # def on_LF(self, node):
    #     return node

    # def on_EOF(self, node):
    #     return node



compiling: Junction = create_junction(
    dioCompiler, "AST", "dio")


#######################################################################
#
# END OF DHPARSER-SECTIONS
#
#######################################################################

#######################################################################
#
# Post-Processing-Stages [add one or more postprocessing stages, here]
#
#######################################################################

# class PostProcessing(Compiler):
#     ...

# # change the names of the source and destination stages. Source
# # ("dio") in this example must be the name of some earlier stage, though.
# postprocessing: Junction = create_junction(PostProcessing, "dio", "refined")
#
# DON'T FORGET TO ADD ALL POSTPROCESSING-JUNCTIONS TO THE GLOBAL
# "junctions"-set IN SECTION "Processing-Pipeline" BELOW!

#######################################################################
#
# Processing-Pipeline
#
#######################################################################

# Add your own stages to the junctions and target-lists, below
# (See DHParser.compile for a description of junctions)

# ADD YOUR OWN POST-PROCESSING-JUNCTIONS HERE:
junctions = set([ASTTransformation, compiling])

# put your targets of interest, here. A target is the name of result (or stage)
# of any transformation, compilation or postprocessing step after parsing.
# Serializations of the stages listed here will be written to disk when
# calling process_file() or batch_process() and also appear in test-reports.
targets = end_points(junctions)
# alternative: targets = set([compiling.dst])

# provide a set of those stages for which you would like to see the output
# in the test-report files, here. (AST is always included)
test_targets = set(j.dst for j in junctions)
# alternative: test_targets = targets

# add one or more serializations for those targets that are node-trees
serializations = expand_table(dict([('*', [get_config_value('default_serialization')])]))


#######################################################################
#
# Main program
#
#######################################################################

def compile_src(source: str, target: str = "dio") -> Tuple[Any, List[Error]]:
    """Compiles the source to a single target and returns the result of the compilation
    as well as a (possibly empty) list or errors or warnings that have occurred in the
    process.

    :param srouce: Either a file name or a source text. Anything that is not a valid
        file name is assumed to be a source text. Add a byte-order mark ("\ufeff")
        at the beginning of short, i.e. one-line source texts, to avoid these being
        misinterpreted as filenames.
    :param target: the name of the target stage up to which the processing pipeline
        will be proceeded.

    :returns: a tuple (data, list of errors) of the data in the format of the
        target-stage selected by parameter "target" and of the potentially
        empty list of errors.
    """
    full_compilation_result = full_pipeline(
        source, preprocessing.factory, parsing.factory, junctions, set([target]))
    return full_compilation_result[target]


def compile_snippet(source_code: str, target: str = "LKS") -> Tuple[Any, List[Error]]:
    """Compiles a piece of source_code. In contrast to :py:func:`compile_src` the
    parameter source_code is always understood as a piece of source-code and never
    as a filename, not even if it is a one-liner that could also be a file-name.
    """
    if source_code[0:1] not in ('\ufeff', '\ufffe') and \
            source_code[0:3] not in ('\xef\xbb\xbf', '\x00\x00\ufeff', '\x00\x00\ufffe'):
        source_code = '\ufeff' + source_code  # add a byteorder-mark for disambiguation
    return compile_src(source_code)


def process_file(source: str, out_dir: str = '') -> str:
    """Compiles the source and writes the serialized results back to disk,
    unless any fatal errors have occurred. Error and Warning messages are
    written to a file with the same name as `result_filename` with an
    appended "_ERRORS.txt" or "_WARNINGS.txt" in place of the name's
    extension. Returns the name of the error-messages file or an empty
    string, if no errors or warnings occurred.
    """
    global serializations
    serializations = get_config_value('dio_serializations', serializations)
    return dsl.process_file(source, out_dir, preprocessing.factory, parsing.factory,
                            junctions, targets, serializations)


def _process_file(args: Tuple[str, str]) -> str:
    return process_file(*args)


def batch_process(file_names: List[str], out_dir: str,
                  *, submit_func: Callable = None,
                  log_func: Callable = None,
                  cancel_func: Callable = never_cancel) -> List[str]:
    """Compiles all files listed in file_names and writes the results and/or
    error messages to the directory `our_dir`. Returns a list of error
    messages files.
    """
    return dsl.batch_process(file_names, out_dir, _process_file,
        submit_func=submit_func, log_func=log_func, cancel_func=cancel_func)


def main(called_from_app=False) -> bool:
    # recompile grammar if needed
    scriptpath = os.path.abspath(os.path.realpath(__file__))
    if scriptpath.endswith('Parser.py'):
        grammar_path = scriptpath.replace('Parser.py', '.ebnf')
    else:
        grammar_path = os.path.splitext(scriptpath)[0] + '.ebnf'
    parser_update = False

    def notify():
        nonlocal parser_update
        parser_update = True
        print('recompiling ' + grammar_path)

    if os.path.exists(grammar_path) and os.path.isfile(grammar_path):
        if not recompile_grammar(grammar_path, scriptpath, force=False, notify=notify):
            error_file = os.path.basename(__file__)\
                .replace('Parser.py', '_ebnf_MESSAGES.txt')
            with open(error_file, 'r', encoding="utf-8") as f:
                print(f.read())
            sys.exit(1)
        elif parser_update:
            if '--dontrerun' in sys.argv:
                print(os.path.basename(__file__) + ' has changed. '
                      'Please run again in order to apply updated compiler')
                sys.exit(0)
            else:
                import platform, subprocess
                call = ['python', __file__, '--dontrerun'] + sys.argv[1:]
                result = subprocess.run(call, capture_output=True)
                print(result.stdout.decode('utf-8'))
                sys.exit(result.returncode)
    else:
        print('Could not check whether grammar requires recompiling, '
              'because grammar was not found at: ' + grammar_path)

    from argparse import ArgumentParser
    parser = ArgumentParser(description="Parses a dio-file and shows its syntax-tree.")
    parser.add_argument('files', nargs='*' if called_from_app else '+')
    parser.add_argument('-d', '--debug', action='store_const', const='debug',
                        help='Store debug information in LOGS subdirectory')
    parser.add_argument('-o', '--out', nargs=1, default=['out'],
                        help='Output directory for batch processing')
    parser.add_argument('-v', '--verbose', action='store_const', const='verbose',
                        help='Verbose output')
    parser.add_argument('-f', '--force', action='store_const', const='force',
                        help='Write output file even if errors have occurred')
    parser.add_argument('--singlethread', action='store_const', const='singlethread',
                        help='Run batch jobs in a single thread (recommended only for debugging)')
    parser.add_argument('--dontrerun', action='store_const', const='dontrerun',
                        help='Do not automatically run again if the grammar has been recompiled.')
    parser.add_argument('-s', '--serialize', nargs='+', default=[])

    args = parser.parse_args()
    file_names, out, log_dir = args.files, args.out[0], ''

    if args.serialize:
        serializations['*'] = args.serialize
        access_presets()
        set_preset_value('dio_serializations', serializations, allow_new_key=True)
        finalize_presets()

    if args.debug is not None:
        log_dir = 'LOGS'
        access_presets()
        set_preset_value('history_tracking', True)
        set_preset_value('resume_notices', True)
        set_preset_value('log_syntax_trees', frozenset(['CST', 'AST']))  # don't use a set literal, here!
        finalize_presets()
    start_logging(log_dir)

    if args.singlethread:
        set_config_value('batch_processing_parallelization', False)

    def echo(message: str):
        if args.verbose:
            print(message)

    if called_from_app and not file_names:  return False

    batch_processing = True
    if len(file_names) == 1:
        if os.path.isdir(file_names[0]):
            dir_name = file_names[0]
            echo('Processing all files in directory: ' + dir_name)
            file_names = [os.path.join(dir_name, fn) for fn in os.listdir(dir_name)
                          if os.path.isfile(os.path.join(dir_name, fn))]
        elif not ('-o' in sys.argv or '--out' in sys.argv):
            batch_processing = False

    if batch_processing:
        if not os.path.exists(out):
            os.mkdir(out)
        elif not os.path.isdir(out):
            print('Output directory "%s" exists and is not a directory!' % out)
            sys.exit(1)
        error_files = batch_process(file_names, out, log_func=print if args.verbose else None)
        if error_files:
            category = "ERRORS" if any(f.endswith('_ERRORS.txt') for f in error_files) \
                else "warnings"
            print("There have been %s! Please check files:" % category)
            print('\n'.join(error_files))
            if category == "ERRORS":
                sys.exit(1)
    else:
        result, errors = compile_src(file_names[0])

        if not errors or (not has_errors(errors, ERROR)) \
                or (not has_errors(errors, FATAL) and args.force):
            print(result.serialize(serializations['*'][0])
                  if isinstance(result, Node) else result)
            if errors:  print('\n---')

        for err_str in canonical_error_strings(errors):
            print(err_str)
        if has_errors(errors, ERROR):  sys.exit(1)

    return True


if __name__ == "__main__":
    main()
