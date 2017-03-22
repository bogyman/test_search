from itertools import groupby

from mario.utils.data_source import *
from mario.node_manager.nodes_holder import NodesHolder
from node.indexer import make_document



documents = ['2ba18bc6ab8dae023a9e73cfc144bed8', 'ebca7e9e3c60801e552fcc84129decc9', 'f645b30e21abaed407ce1a288729b272', '7892f28b515ca660e467b55a0543bf7b', '12bd376797d9c53678153b90a330b483', '4b5c11f7664bb2c281b65fe3ecf1215d', '0d843ad3626775a4770e36d9d2b41931', 'f67129b6174539abf33db4d873d0a96f', '05024ceaa4712d7a751c7c27d95abc08', '6e3a4f4bbaab01564cf65feb083d64f5', 'dbb7301ff1430bc0e57290e71b50fa45', '3fe5c0810556700fa73608c3f32a1bb2', '72a3f62fcfc8e67fa69a604f3353bcbf', 'acc3cde56097997d8402ba648fbf7ad7', '7dd3a4dc297b1877f6021e85870df203', '9ba568992e41353a3a6bc167608bd86a', '83c57afd0b74bb41083304a6cb86a8b2', 'eef65a664eca34fa01a8273b34353dbe', '92ab8b123863d7b4f7115bbd0fd4f83f', 'b76e693716e3c1c00a382257944dfaf2', 'd76ad2e6633c7bcfb33f193212e211b4', '06a57f42e8ab95821094ca52650908ca', '5b3792103dabfa7acd7ec01e77880df6', 'f55f5848283b86219c0d954ceb38f9c6', 'f36016747c98f85af2c6d08990f6fcfa', '2dc13cbb52173446dafc918425180290', '39e872a417ca807dcb755d928f333f1e', '37631b4a872ddb9f0904f8222156d636', '07cb305c5ee94bd437886aaa22bab75b', '0db476d99952ce053d4e3c01a2af1931', 'd478349cee2a15a92d5b39f4587a115e', '252e4061b12b711a93cde03b5650ffa0', '286ce109e3315e00ed45eb57f54fa362', '6a1541e76d603242cf61a73dd0a7b9d3', 'cf2665726af8b5b415058207639ea3ee', '67f869e99f2cd29efc66785e5e07b091', '10b08757cf685ea2f510e2ec9c80a759', 'effc0e8a3d53b982d2158fc54abb404f', 'e3e145bb571e729557caf200dc6a2961', '9a1e9b32a889cb810927dd1c70d82510', '774e5cff4079df4ea81b4e457b5128f9', '6e6797ee48f06bed849c266beb429f9c', '06c56c80c41ff8e5f79b386fd4078aaa', 'e9b0761d094fed0ab422cc03425f2f63', '8dec27cb0f37b41175d61334480b1341', 'b226fabd88a7f5c1bffbbd6ad0250901', '75f36058fb06d265f372a4bfc473a146', '2c8fde9e6f49db858d2b0980b2a5f314', '7c26ce04b77906be259aee18e968d303', '89b46deb5231c3ffb0e06e7dfb050dd4', '116704bc4b58ee56febfa324abe851cb', 'bee151ad21157c3173b2c4863cdac443', 'a44e6125267654b1e624463e9e288631', 'abb152c004fd0838a1d3050f17b81259', 'd0cabe55c27739c046ad07e5a356cafe', '11add0ba07634c4e927ab65ace8048cf', 'b6efbd22d9970b8e2a4906062e282085', '0ca23dfeb10fbea627ffc66fcd9a4833', 'fedcef05f4c9d43db838b20b17445240', '33332919c6933136f94f2aedbcb3323d', 'daf8bf15010ff105146e261ef54c54ed', 'd7c7a4a210d8902def5ea35358f5266a', 'd41452e42653a0d5874e2bccff4fb422', '094583aee83ed14504ec40e159b7fcb8', '97f1b3191309042cdce5da88a1a21ae1', '0d823c77bd591238bffe273a36f941e5', 'a9dda400bd3e25a1a377924ba2b6ba10', '93050701d609cd5b9b1c5ab05e30872a', '9877f17ba01f2615f6d8bd452cb612c6', '4ca0fc13bd24e2996de195c4517d3359', '8fd4c22a370c73903ef697e4bd53df48', '104bf7418a87faa0be7267b3b03063b4', 'fb72c4d254080576f2a2b0d9157ebb51', 'afeb22741d2e0bb01349af054bee5990', '1d4966dccf2e5127bf5e2711b8183f0a', 'd03c182ec29ddf743aca7c69af571bd5', '979b1c58394e0f25281636ad8a56ed81', 'f961fb8be10fc009701fb98c9f7fd91c', '54ff5172114c26c9b808b0cf3b4c4e27', '3d5b178e00031ea53fde1b7bf0e04193', '229d998575a9545686c7cc230171cdd5', '1131f8e11a64bd33ced8ac0d563e20c2', '7860548200540d44a38c9525c07ffd1e', 'c5a20add8c3abf98ad38f5802b32ee47', 'c379006531d9aa52d81ae1c08489bd5f', '76bfc2bade0409886a8acf480f318238', '3ca156319558a6e6dd88b799a2ef3127', '0b793b8ab2ae85ecc5e6f9b7e8de5ca4', '7a7aff121c2f1b3d44d2be03a56c7543', 'ab720182482630ab49a6872aec7ad413', '0247973d8531b4cd8ee43834c857d439', '8cfcac40ce4f39342dfad8df4dc0f654', 'b020a251d5c4d7329ff5dcc6ab11af28', '30b2229842fc3cfe7f7c57bd6a574015', 'd0f8904c41c5bf2bbbfab336cd2c2b32', 'f17309b60a35e05d21732dd5a996102a', '0043f2fe818e754ff339756a41fa13cf', '107720fcce8657e810639f5b727c81d3', '2ba9d07514e6c11fa69c3064a3be7714']

def test_index():
    pass


def test_search():
    pass


def test_utils():
    a = fetch_resources()
    NodesHolder.add_node('333333')
    NodesHolder.add_node('40000')
    NodesHolder.add_node('4----')
    b = get_nodes_offsets(NodesHolder, a)
    c = get_nodes_tasks(b)
    print(c)

def test_make_document():
    item = {'deck': 'A Chibi Maruko-Chan boardgame for Super Nintendo.', 'image': {'icon_url': 'http://www.giantbomb.com/api/image/square_avatar/1688275-chibi_maruko_chan_harikiri_365_nichi_no_maki_box_front.jpg', 'medium_url': 'http://www.giantbomb.com/api/image/scale_medium/1688275-chibi_maruko_chan_harikiri_365_nichi_no_maki_box_front.jpg', 'screen_url': 'http://www.giantbomb.com/api/image/screen_medium/1688275-chibi_maruko_chan_harikiri_365_nichi_no_maki_box_front.jpg', 'small_url': 'http://www.giantbomb.com/api/image/scale_small/1688275-chibi_maruko_chan_harikiri_365_nichi_no_maki_box_front.jpg', 'super_url': 'http://www.giantbomb.com/api/image/scale_large/1688275-chibi_maruko_chan_harikiri_365_nichi_no_maki_box_front.jpg', 'thumb_url': 'http://www.giantbomb.com/api/image/scale_avatar/1688275-chibi_maruko_chan_harikiri_365_nichi_no_maki_box_front.jpg', 'tiny_url': 'http://www.giantbomb.com/api/image/square_mini/1688275-chibi_maruko_chan_harikiri_365_nichi_no_maki_box_front.jpg'}, 'name': 'Chibi Maruko-Chan: Harikiri 365-Nichi no Maki', 'platforms': [{'api_detail_url': 'http://www.giantbomb.com/api/platform/3045-9/', 'id': 9, 'name': 'Super Nintendo Entertainment System', 'site_detail_url': 'http://www.giantbomb.com/super-nintendo-entertainment-system/3045-9/', 'abbreviation': 'SNES'}], 'site_detail_url': 'http://www.giantbomb.com/chibi-maruko-chan-harikiri-365-nichi-no-maki/3030-33958/'}
    make_document(item)



def test_scores():
    dict([(i, len(list(j))) for i, j in groupby(documents)])