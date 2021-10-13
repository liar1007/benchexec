import benchexec.result as result
import benchexec.tools.template


class Tool(benchexec.tools.template.BaseTool2):
    """
    Theta
    A generic, modular and configurable model checking framework developed at the Critical Systems Research Group of Budapest University of Technology and Economics, aiming to support the design and evaluation of abstraction refinement-based algorithms for the reachability analysis of various formalisms.

    https://github.com/ftsrg/theta
    """

    REQUIRED_PATHS = [".."]

    def executable(self, tool_locator):
        return tool_locator.find_executable("theta-start.sh", subdir="")

    def name(self):
        return "theta"

    def version(self, executable):
        return self._version_from_tool(executable)

    def cmdline(self, executable, options, task, rlimits):
        return (
            [executable] + [task.single_input_file] + options
        )  # we only support unreach-call

    def determine_result(self, run):
        status = result.RESULT_UNKNOWN
        for line in run.output:
            if "SafetyResult Unsafe" in line:
                status = result.RESULT_FALSE_PROP
            if "SafetyResult Safe" in line:
                status = result.RESULT_TRUE_PROP

        if (
            not run.was_timeout
            and status == result.RESULT_UNKNOWN
            and run.exit_code.value != 0
        ):
            if run.exit_code.value == 226:
                status = "ERROR (verification stuck)"
            elif run.exit_code.value == 137:
                status = "OUT_OF_MEMORY"
            elif run.exit_code.value == 206:
                status = "ERROR (unable to transform XCFA to CFA)"
            elif run.exit_code.value == 176:
                status = "ERROR (frontend failed)"
            elif run.exit_code.value == 213:
                status = "ERROR (portfolio timeout)"
            else:
                status = result.RESULT_ERROR

        return status
