import logger_utils

from flask import Flask, request, jsonify, Response

from check_solution import SolutionTests

# Set logging
logger = logger_utils.setup_applevel_logger()

app = Flask(__name__)


def get_score(percentage):
    """ Return score from percentage for learning outcome. """
    if percentage >= 95:
        result = 5
    elif percentage >= 80:
        result = 4
    elif percentage >= 70:
        result = 3
    else:
        result = 2

    return result


@app.route('/do-dynamic-tests/', methods=['GET'])
@app.route('/do-dynamic-tests', methods=['GET'])
def dynamic_testing():
    data = request.get_json()

    if not data:
        return Response(status=404)

    url: str = data.get('github_url')
    if not url:
        return Response(status=404)
    if not url.startswith('https://github.com/'):
        return jsonify({
            'github_url': url,
            'result': 'error'
        })

    logger.info(f'New url: {url}')

    solution = SolutionTests(url)
    """try:
        result, access_time = solution.run_tests()
    except Exception:
        return jsonify({'github_url': url,
                        'result': 'error', })"""

    result, access_time = solution.run_tests()

    if isinstance(result, bool) or isinstance(access_time, bool):
        return jsonify({
            'github_url': url,
            'result': 'error'
        })

    result = get_score(result)
    access_time = get_score(access_time)

    return jsonify({
        'github_url': url,
        'result': result,
        'access_time': access_time
    })


if __name__ == '__main__':
    app.run(port=6000, debug=True)
