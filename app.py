
from flask import Flask, render_template, request, jsonify, send_file, make_response, url_for, Response

#Pandas and Matplotlib
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
import io
from sklearn.neighbors import NearestNeighbors
import base64
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob
import matplotlib.cbook as cbook
from matplotlib_scalebar.scalebar import ScaleBar
import scanpy as sc
import matplotlib.font_manager
import os
import numpy as np
import json
import linecache
import pylab
import time
import matplotlib.patheffects as path_effects
from werkzeug.exceptions import HTTPException



#other requirements
import io

app = Flask(__name__)

STATIC_FOLDER = os.path.join('static', 'images')
GLOBAL_COUNT1 = "0 hr Avrrpt"
GLOBAL_COUNT2 = "Multiome"
GLOBAL_COUNT1_PSEUDO = "0 hr Avrrpt"
GLOBAL_COUNT2_PSEUDO = "Multiome"
GLOBAL_IMPUTED_CURRENT = "0 hr Avrrpt"
GLOBAL_MOTIF_CURRENT = "0 hr Avrrpt"
GENE_LIST = np.load("static/detected_transcripts/gene_list.npy")
MYOPTION = np.load('static/detected_transcripts/gene_interest.npy')
IMPUTED_NAMES = np.load('static/detected_transcripts/imputed_names.npy')
MOTIF_NAMES = np.load('static/detected_transcripts/motif_names.npy')
STARTED = False


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = STATIC_FOLDER


@app.route('/viewer')
def viewer():
    return render_template("viewer.html")

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def show_index():
    global GLOBAL_COUNT1
    global STARTED
    global GLOBAL_COUNT2
    global GLOBAL_COUNT1_PSEUDO
    global GLOBAL_COUNT2_PSEUDO
    global CURRENT_PSEUDOTIME
    global GLOBAL_IMPUTED_CURRENT
    global GLOBAL_MOTIF_CURRENT


    time1 = time.time()
    if request.method == "POST":
        columnars = request.get_json()
        columnars = columnars[0]
        print(columnars)
        if len(list(columnars.keys())) == 2:
            if columnars.get(list(columnars.keys())[0]) == columnars.get(list(columnars.keys())[1]):
                return json.dumps({'saver1': os.path.join(app.config['UPLOAD_FOLDER'], 'warning_diff.png')}) 
            return create_differential(columnars.get(list(columnars.keys())[0]), columnars.get(list(columnars.keys())[1]))
        elif len(list(columnars.keys())) == 3:
            ex = columnars.get(list(columnars.keys())[0])
            gene = columnars.get(list(columnars.keys())[1])
            print(gene)
            if gene[0] == 'alex':
                return get_ax_imp(ex, gene, True)
            else:
                button = columnars.get(list(columnars.keys())[2])
                if button == 'button':
                    ex = GLOBAL_IMPUTED_CURRENT
                else:
                    GLOBAL_IMPUTED_CURRENT = ex
                return get_ax_imp(ex, gene, False)
        elif len(list(columnars.keys())) == 4:
            ex = columnars.get(list(columnars.keys())[0])
            gene = columnars.get(list(columnars.keys())[1])
            button = columnars.get(list(columnars.keys())[2])
            if gene[0] == 'alex':
                return get_ax_motif(ex, gene[0], True)
            if button == 'button':
                ex = GLOBAL_MOTIF_CURRENT
            else:
                GLOBAL_MOTIF_CURRENT = ex
            return get_ax_motif(ex, gene, False)   
        bacteria = columnars.get(list(columnars.keys())[-7])          
        pseudotime_exp1 = columnars.get(list(columnars.keys())[-6])
        pseudotime_exp2 = columnars.get(list(columnars.keys())[-5])
        pseudotime = columnars.get(list(columnars.keys())[-4])
        expval1 = columnars.get(list(columnars.keys())[-2])
        expval2 = columnars.get(list(columnars.keys())[-1])
        transcripts = columnars.get(list(columnars.keys())[-3])
        if expval1 != "current":
            GLOBAL_COUNT1 = expval1
        if pseudotime_exp1 != "current":
            GLOBAL_COUNT1_PSEUDO = pseudotime_exp1
        if expval2 != "current":
            GLOBAL_COUNT2 = expval2
        if pseudotime_exp2 != "current":
            GLOBAL_COUNT2_PSEUDO = pseudotime_exp2
    elif request.method == "GET":
        columnars = {"num0": 1, "num1": 1, "num2": 1, "num3": 1, "num4": 1, "num5": 1, "num6": 1, "num7": 1, "num8": 1, "num9": 1, "num10": 1, "num11": 1, "num12": 1, "num13": 1, "num14": 1, "num15": 1, "num16": 1, "num17": 1, "bacteria": 0, "p_experiment": GLOBAL_COUNT1_PSEUDO, "p_experiment2": GLOBAL_COUNT2_PSEUDO, "pseudotime":"raw", "Transcripts": "None", "experiment": GLOBAL_COUNT1, "experiment2": GLOBAL_COUNT2}
        transcripts = []
        pseudotime = 'raw'
        CURRENT_PSEUDOTIME = "raw"
    time2 = time.time()
    #else:
    #    return render_template("index.html", user_image = os.path.join(app.config['UPLOAD_FOLDER'], 'plot2.png'))
    axis1 = 'mer'
    axis2 = 'mer'
    if GLOBAL_COUNT1 == '0 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/0 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT1 == '4 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/4 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT1 == '6 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/6 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT1 == '9 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/9 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT1 == '24 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/24 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT1 == '24 hr Kt56':
        new_adata = sc.read('scanpy_objects/24 hr Kt56.h5ad')
    elif GLOBAL_COUNT1 == 'Multiome':
        new_adata = sc.read('scanpy_objects/multiome_for_final.h5ad')
        axis1 = 'rna'
    else:
        print(GLOBAL_COUNT1)
        new_adata = sc.read('scanpy_objects/0 hr Avrrpt.h5ad')

    if GLOBAL_COUNT2 == '0 hr Avrrpt':
        new_adata2 = sc.read('scanpy_objects/0 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT2 == '4 hr Avrrpt':
        new_adata2 = sc.read('scanpy_objects/4 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT2 == '6 hr Avrrpt':
        new_adata2 = sc.read('scanpy_objects/6 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT2 == '9 hr Avrrpt':
        new_adata2 = sc.read('scanpy_objects/9 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT2 == '24 hr Avrrpt':
        new_adata2 = sc.read('scanpy_objects/24 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT2 == '24 hr Kt56':
        new_adata2 = sc.read('scanpy_objects/24 hr Kt56.h5ad')
    elif GLOBAL_COUNT2 == 'Multiome':
        new_adata2 = sc.read('scanpy_objects/multiome_for_final.h5ad')
        axis2 = 'rna'
    else:
        print(GLOBAL_COUNT2)
        new_adata2 = sc.read('scanpy_objects/multiome_for_final.h5ad')
    if pseudotime == 'current':
        pseudotime = CURRENT_PSEUDOTIME
    if (pseudotime == 'none') or request.method == "GET":
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (10,4),dpi = 400, facecolor='None')
        if axis1 == 'mer':
            ax1 = get_ax_merfish(new_adata, ax1, columnars, GLOBAL_COUNT1)
        else:
            ax1 = get_rna_merfish(new_adata, ax1, columnars)

        ax1 = display_trans(ax1, transcripts, GLOBAL_COUNT1)
        #legend = ax1.legend()
        ax1.axis('off')
        # create a second figure for the legend
        if len(transcripts) > 0:
            figLegend = pylab.figure(figsize = (1.5,1.3))

            # produce a legend for the objects in the other figure

            lege = pylab.figlegend(*ax1.get_legend_handles_labels(), loc = 'center', fontsize=8, labelcolor='black')
            for k in [0, 1, 2]:
                try:
                    lege.legendHandles[k]._sizes = [50]
                except:
                    None
            figLegend.suptitle('Legend', color = 'black')
            figLegend.set_facecolor('floralwhite')

            #figLegend.savefig("static/images/legend.png")
        else:
            figLegend = pylab.figure(figsize = (1.5,1.3))

        #ax1.legend().set_visible(False)
        if axis2 == 'mer':
            ax2 = get_ax_merfish(new_adata2, ax2, columnars, GLOBAL_COUNT2)
        else:
            ax2 = get_rna_merfish(new_adata2, ax2, columnars)
        ax2 = display_trans(ax2, transcripts, GLOBAL_COUNT2)
        ax2.legend().set_visible(False)
        #txt.set_path_effects([path_effects.withStroke(linewidth=0.5, foreground='k')])
        #txt.set_path_effects([path_effects.withStroke(linewidth=0.5, foreground='k')])
        ax2.axis('off')

        if request.method == "GET": 
            extent1 = ax1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            extent2 = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            fig.savefig(os.path.join(app.config['UPLOAD_FOLDER'], 'plot2.png'), dpi = 400, bbox_inches=extent1)
            fig.savefig(os.path.join(app.config['UPLOAD_FOLDER'], 'plot3.png'), dpi = 400, bbox_inches=extent2)
            figLegend = pylab.figure(figsize = (1.5,1.3))
            figLegend.set_facecolor('floralwhite')
            figLegend.savefig(os.path.join(app.config['UPLOAD_FOLDER'], 'legend.png'), dpi = 400)
            
            fig, (ax3, ax4) = plt.subplots(1, 2, figsize = (10,4),dpi = 400, facecolor='None')
            if axis1 == 'mer':
                ax3, hold = get_ax_pseudo(new_adata, ax3, GLOBAL_COUNT1, 'raw')
            else:
                ax3 = get_ax_rnapseudo(new_adata, ax3)
            #legend = ax1.legend()

            ax3.axis('off')

            if axis2 == 'mer':
                ax4, hold = get_ax_pseudo(new_adata2, ax4, GLOBAL_COUNT2, 'raw')
            else:
                ax4 = get_ax_rnapseudo(new_adata2, ax4)
            
            ax4.axis('off')

            extent1 = ax3.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            extent2 = ax4.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            fig.savefig(os.path.join(app.config['UPLOAD_FOLDER'], 'p_plot1.png'), dpi = 400, bbox_inches=extent1)
            fig.savefig(os.path.join(app.config['UPLOAD_FOLDER'], 'p_plot2.png'), dpi = 400, bbox_inches=extent2)

        else:
            try:
                list_files = glob.glob('static/images/plot2*.png')
                for fl in list_files:
                    os.remove(fl)
                list_files = glob.glob('static/images/plot3*.png')
                for fl in list_files:
                    os.remove(fl)
                list_files = glob.glob('static/images/legend*.png')
                for fl in list_files:
                    os.remove(fl)
            except Exception as e: print(e)
            saver1 = os.path.join(app.config['UPLOAD_FOLDER'], 'plot2'+str(time.time()).replace('.', '')+'.png')
            saver2 = os.path.join(app.config['UPLOAD_FOLDER'], 'plot3'+str(time.time()).replace('.', '')+'.png')
            saveleg = os.path.join(app.config['UPLOAD_FOLDER'], 'legend'+str(time.time()).replace('.', '')+'.png')
            extent1 = ax1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            extent2 = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            fig.savefig(saver1, dpi = 400, bbox_inches=extent1)
            fig.savefig(saver2, dpi = 400, bbox_inches=extent2)

            figLegend.savefig(saveleg, dpi = 400)
            # out = BytesIO()
            # cairosvg.svg2png(url=saver, write_to=out)
            # image = Image.open(out)
            # image.save(saver.split('.')[0]+'.png')
        if request.method == "GET": 
            img1_path, img2_path = get_ax_imp('0 hr Avrrpt', None, True)
            GLOBAL_IMPUTED_CURRENT = "0 hr Avrrpt"
            STARTED = True
            return render_template("index.html", motif_names = MOTIF_NAMES, imputed_names = IMPUTED_NAMES, myOptions = MYOPTION, second_image = os.path.join(app.config['UPLOAD_FOLDER'], 'legend.png'), user_imageax1 = os.path.join(app.config['UPLOAD_FOLDER'], 'plot2.png'), user_imageax2 = os.path.join(app.config['UPLOAD_FOLDER'], 'plot3.png'), user_imageax1p = os.path.join(app.config['UPLOAD_FOLDER'], 'p_plot1.png'), user_imageax2p = os.path.join(app.config['UPLOAD_FOLDER'], 'p_plot2.png'), user_imageax1_diff = os.path.join(app.config['UPLOAD_FOLDER'], 'plot3.png'), df = os.path.join(app.config['UPLOAD_FOLDER'], 'warning_diff.png'), colorbar = os.path.join(app.config['UPLOAD_FOLDER'], 'colobar.png'), user_imageax1_imp = img1_path, user_imageax2_imp = img2_path, user_imageax1_motif = img1_path, user_imageax2_motif = img2_path)
        else:
            return json.dumps({'saver1': saver1, 'saver2': saver2, 'saveleg': saveleg})
    else:
        axis1, axis2, new_adata, new_adata2 = return_pseudo_experiment()
        fig, (ax3, ax4) = plt.subplots(1, 2, figsize = (10,4),dpi = 400, facecolor='None')
        if axis1 == 'mer':
            ax3, hold = get_ax_pseudo(new_adata, ax3, GLOBAL_COUNT1_PSEUDO, pseudotime)
        else:
            ax3 = get_ax_rnapseudo(new_adata, ax3)
        #cbar = fig.colorbar(hold, ax=ax3)
        #legend = ax1.legend()
        # if GLOBAL_COUNT1 == '24 hr Avrrpt':
        #     fig2,ax = plt.subplots(figsize=(10, 4)) 
        #     fig2.set_facecolor('floralwhite')
        #     fig2.colorbar(hold,ax=ax)
        #     ax.remove()
        #     fig2.savefig('static/images/colobar.png')
        ax3.axis('off')

        if axis2 == 'mer':
            ax4, hold = get_ax_pseudo(new_adata2, ax4, GLOBAL_COUNT2_PSEUDO, pseudotime)
        else:
            ax4 = get_ax_rnapseudo(new_adata2, ax4)
        
        ax4.axis('off')

        extent1 = ax3.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        extent2 = ax4.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

        try:
            list_files = glob.glob('static/images/p_plot1*.png')
            for fl in list_files:
                os.remove(fl)
            list_files = glob.glob('static/images/p_plot2*.png')
            for fl in list_files:
                os.remove(fl)
        except:
            None
        saver1 = os.path.join(app.config['UPLOAD_FOLDER'],'p_plot1'+str(time.time()).replace('.', '')+'.png')
        saver2 = os.path.join(app.config['UPLOAD_FOLDER'], 'p_plot2'+str(time.time()).replace('.', '')+'.png')
        fig.savefig(saver1, dpi = 400, bbox_inches=extent1)
        fig.savefig(saver2, dpi = 400, bbox_inches=extent2)
        return json.dumps({'saver1': saver1, 'saver2': saver2})

def get_ax_motif(exp, gene, getter):
    try:
        list_files = glob.glob('static/images/motif_plotd*.png')
        for fl in list_files:
            os.remove(fl)
    except:
        None
    if exp != 'Multiome':
        if (getter == False) and (len(gene) > 0):
            new_adata = get_adata_from_exp(exp) 
            fig, ax1 = plt.subplots(1, 1)
            ax1.set_facecolor('floralwhite')
            m = new_adata.obsm['X_spatial']
            motif = gene[0].split('_')
            motif = motif[1] + '_' + motif[0] + '_' + 'transfer'

            if gene == None:
                hold = ax1.scatter(m.T[0], m.T[1], label='_nolegend_', c = 'gray', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 1, vmax = 0.6, vmin = 0)
            else:
                vals = np.array(new_adata[:, new_adata.var.index.isin([motif])].X.T[0])
                hold = ax1.scatter(m.T[0], m.T[1], label='_nolegend_', c = vals, cmap='coolwarm', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 1, vmax = np.max([np.percentile(vals, 98)]), vmin = np.max([np.percentile(vals, 2)]))
                plt.colorbar(hold)

            if exp != '9 hr Avrrpt':
                scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper right', box_color="floralwhite")
            else:
                scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper left', box_color="floralwhite")
            ax1.add_artist(scalebar)
            ax1.grid(False)
            ax1.set_yticks([])
            ax1.set_xticks([])
            ax1.axis('off')
            
            saverx = os.path.join(app.config['UPLOAD_FOLDER'], 'motif_plotd'+str(time.time()).replace('.', '')+'.png')
            fig.savefig(saverx, dpi = 400, bbox_inches='tight', facecolor='floralwhite')
            plt.close()
        

            fig, ax2 = plt.subplots(1, 1)
            ax2.set_facecolor('floralwhite')
            m = new_adata.obsm['X_spatial']
            motif = gene[0].split('_')
            motif = motif[1] + '_' + motif[0] + '_' + 'transfer'

            if gene == None:
                hold = ax2.scatter(m.T[0], m.T[1], label='_nolegend_', c = 'gray', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 1, vmax = 0.6, vmin = 0)
            else:
                vals = np.array(new_adata[:, new_adata.var.index.isin([motif])].X.T[0])
                hold = ax2.scatter(m.T[0], m.T[1], label='_nolegend_', c = vals, cmap='coolwarm', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 1, vmax = np.max([np.percentile(vals, 98)]), vmin = np.max([np.percentile(vals, 2)]))

            if exp != '9 hr Avrrpt':
                scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper right', box_color="floralwhite")
            else:
                scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper left', box_color="floralwhite")
            ax2.add_artist(scalebar)
            ax2.grid(False)
            ax2.set_yticks([])
            ax2.set_xticks([])
            ax2.axis('off')
            savery = os.path.join(app.config['UPLOAD_FOLDER'], 'motif_plotd'+str(time.time()).replace('.', '')+'.png')
            fig.savefig(savery, dpi = 400, bbox_inches='tight', facecolor='floralwhite')
            plt.close()
            return json.dumps({'saver1': saverx, 'saver2': savery})
        else:
            new_adata = get_adata_from_exp(exp) 
            fig, ax1 = plt.subplots(1, 1)
            ax1.set_facecolor('floralwhite')
            m = new_adata.obsm['X_spatial']
            
            hold = ax1.scatter(m.T[0], m.T[1], label='_nolegend_', color = 'gray', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 0.2, vmax = 0.6, vmin = 0)

            if exp != '9 hr Avrrpt':
                scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper right', box_color="floralwhite")
            else:
                scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper left', box_color="floralwhite")
            ax1.add_artist(scalebar)
            ax1.grid(False)
            ax1.set_yticks([])
            ax1.set_xticks([])
            ax1.axis('off')
            saverx = os.path.join(app.config['UPLOAD_FOLDER'], 'motif_plotd'+str(time.time()).replace('.', '')+'.png').replace('\\', '/')
            fig.savefig(saverx, dpi = 400, bbox_inches='tight', facecolor='floralwhite')
            plt.close()
            if (getter == True) and (gene == None):
                return saverx, saverx
            elif getter == True:
                return json.dumps({'saver1': saverx, 'saver2': saverx})
            else:
                return json.dumps({'saver1': saverx, 'saver2': saverx})
    else:
        if (getter == False) and (len(gene) > 0):
            new_adata = get_adata_from_exp(exp) 
            fig, ax1 = plt.subplots(1, 1)
            ax1.set_facecolor('floralwhite')
            m = new_adata.obsm['X_umap']
            if gene == None:
                hold = ax1.scatter(m.T[0], m.T[1], label='_nolegend_', c = 'gray', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 0.2, vmax = 0.6, vmin = 0)
            else:
                vals = np.array(new_adata[:,np.where(np.array(new_adata.var.index.tolist()) == gene)[0]].X.todense()).T[0]
                hold = ax1.scatter(m.T[0], m.T[1], label='_nolegend_', c = vals, cmap='Greens', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 1, vmax = np.max([0.15, np.percentile(vals, 95)]), vmin = 0)
            
            ax1.grid(False)
            ax1.set_yticks([])
            ax1.set_xticks([])
            ax1.axis('off')
            saverx = os.path.join(app.config['UPLOAD_FOLDER'], 'motif_plotd'+str(time.time()).replace('.', '')+'.png')
            fig.savefig(saverx, dpi = 400, bbox_inches='tight', facecolor='floralwhite')
            plt.close()
        

            savery = saverx
            return json.dumps({'saver1': saverx, 'saver2': savery})
        else:
            new_adata = get_adata_from_exp(exp) 
            fig, ax1 = plt.subplots(1, 1)
            ax1.set_facecolor('floralwhite')
            m = new_adata.obsm['X_umap']
            
            hold = ax1.scatter(m.T[0], m.T[1], label='_nolegend_', c = 'gray', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 1, vmax = 0.6, vmin = 0)

            ax1.grid(False)
            ax1.set_yticks([])
            ax1.set_xticks([])
            ax1.axis('off')
            saverx = os.path.join(app.config['UPLOAD_FOLDER'], 'motif_plotd'+str(time.time()).replace('.', '')+'.png').replace('\\', '/')
            fig.savefig(saverx, dpi = 400, bbox_inches='tight', facecolor='floralwhite')
            plt.close()
            if getter == True:
                return saverx, saverx
            else:
                return json.dumps({'saver1': saverx, 'saver2': saverx})    

def create_differential(cluster1, cluster2):
    try:
        list_files = glob.glob('static/images/p_plotd*.png')
        for fl in list_files:
            os.remove(fl)
    except:
        None
    new_adata = sc.read('scanpy_objects/multiome_for_final.h5ad')
    sc.tl.rank_genes_groups(new_adata, 'SCT_snn_res.1', groups=[cluster1], reference=cluster2, method='wilcoxon')
    fig, ax1 = plt.subplots(1, 1)
    sc.pl.rank_genes_groups_violin(new_adata, groups=cluster1, n_genes=10, ax=ax1, show=False)   
    saverx = os.path.join(app.config['UPLOAD_FOLDER'], 'p_plotd'+str(time.time()).replace('.', '')+'.png')
    ax1.set_title('Cluster '+ cluster1 +' vs. Cluster ' + cluster2 + ' Differential Expression', fontsize = 20)
    ax1.set_xlabel('Top 10 Differentially Expressed Genes', fontsize = 15)
    ax1.set_ylabel('Expression', fontsize = 15)
    fig.savefig(saverx, dpi = 400, bbox_inches='tight')
    plt.close()
    return json.dumps({'saver1': saverx})

def return_pseudo_experiment():
    axis1 = 'mer'
    axis2 = 'mer'
    if GLOBAL_COUNT1_PSEUDO == '0 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/0 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT1_PSEUDO == '4 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/4 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT1_PSEUDO == '6 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/6 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT1_PSEUDO == '9 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/9 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT1_PSEUDO == '24 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/24 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT1_PSEUDO == '24 hr Kt56':
        new_adata = sc.read('scanpy_objects/24 hr Kt56.h5ad')
    elif GLOBAL_COUNT1_PSEUDO == 'Multiome':
        new_adata = sc.read('scanpy_objects/multiome_for_final.h5ad')
        axis1 = 'rna'
    else:
        print(GLOBAL_COUNT1_PSEUDO)
        new_adata = sc.read('scanpy_objects/0 hr Avrrpt.h5ad')

    if GLOBAL_COUNT2_PSEUDO == '0 hr Avrrpt':
        new_adata2 = sc.read('scanpy_objects/0 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT2_PSEUDO == '4 hr Avrrpt':
        new_adata2 = sc.read('scanpy_objects/4 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT2_PSEUDO == '6 hr Avrrpt':
        new_adata2 = sc.read('scanpy_objects/6 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT2_PSEUDO == '9 hr Avrrpt':
        new_adata2 = sc.read('scanpy_objects/9 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT2_PSEUDO == '24 hr Avrrpt':
        new_adata2 = sc.read('scanpy_objects/24 hr Avrrpt.h5ad')
    elif GLOBAL_COUNT2 == '24 hr Kt56':
        new_adata2 = sc.read('scanpy_objects/24 hr Kt56.h5ad')
    elif GLOBAL_COUNT2_PSEUDO == 'Multiome':
        new_adata2 = sc.read('scanpy_objects/multiome_for_final.h5ad')
        axis2 = 'rna'
    else:
        print(GLOBAL_COUNT2_PSEUDO)
        new_adata2 = sc.read('scanpy_objects/multiome_for_final.h5ad')
    return axis1, axis2, new_adata, new_adata2


def display_trans(ax3, transcripts, input_file):
    if transcripts != [] and transcripts != "None":
        colorlist = ['magenta', 'cyan', 'saddlebrown']
        ct = 0
        for i in transcripts:
            place = np.where(GENE_LIST == i)
            print(place)
            if input_file != 'Multiome':
                if input_file == '0 hr Avrrpt':
                    xandy = np.loadtxt('static/detected_transcripts/Mockdetected.txt',skiprows = 1+(place[0][0]*3),max_rows =2)
                    ax3.scatter(xandy[1], xandy[0],  s = 1, marker = '.', color = colorlist[ct], edgecolors=colorlist[ct], linewidths=0.05, label = i)
                elif input_file == '4 hr Avrrpt':
                    xandy = np.loadtxt('static/detected_transcripts/Avr_4detected.txt',skiprows = 1+(place[0][0]*3),max_rows =2)
                    ax3.scatter(xandy[0], xandy[1],  s = 1, marker = '.', color = colorlist[ct], edgecolors=colorlist[ct], linewidths=0.05, label = i)
                elif input_file == '6 hr Avrrpt':
                    xandy = np.loadtxt('static/detected_transcripts/Avr_6detected.txt',skiprows = 1+(place[0][0]*3),max_rows =2)
                    ax3.scatter(xandy[0], xandy[1],  s = 1, marker = '.', color = colorlist[ct], edgecolors=colorlist[ct], linewidths=0.05, label = i)
                elif input_file == '9 hr Avrrpt':
                    xandy = np.loadtxt('static/detected_transcripts/Avr_9detected.txt',skiprows = 1+(place[0][0]*3),max_rows =2) 
                    ax3.scatter(xandy[0], xandy[1],  s = 1, marker = '.', color = colorlist[ct], edgecolors=colorlist[ct], linewidths=0.05, label = i)
                elif input_file == '24 hr Avrrpt':
                    xandy = np.loadtxt('static/detected_transcripts/Avr_24detected.txt',skiprows = 1+(place[0][0]*3),max_rows =2)
                    ax3.scatter(xandy[1], xandy[0],  s = 1, marker = '.', color = colorlist[ct], edgecolors=colorlist[ct], linewidths=0.05, label = i)
                elif input_file == '24 hr Kt56':
                    xandy = np.loadtxt('static/detected_transcripts/KT56detected.txt',skiprows = 1+(place[0][0]*3),max_rows =2)               
                    ax3.scatter(xandy[1], xandy[0],  s = 1, marker = '.', color = colorlist[ct], edgecolors=colorlist[ct], linewidths=0.05, label = i)
            ct += 1
    return ax3

def get_adata_from_exp(expe):
    if expe == '0 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/0 hr Avrrpt.h5ad')
    elif expe == '4 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/4 hr Avrrpt.h5ad')
    elif expe == '6 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/6 hr Avrrpt.h5ad')
    elif expe == '9 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/9 hr Avrrpt.h5ad')
    elif expe == '24 hr Avrrpt':
        new_adata = sc.read('scanpy_objects/24 hr Avrrpt.h5ad')
    elif expe == '24 hr Kt56':
        new_adata = sc.read('scanpy_objects/24 hr Kt56.h5ad')
    elif expe == 'Multiome':
        new_adata = sc.read('scanpy_objects/multiome_for_final.h5ad')    
    return new_adata

def get_ax_imp(exp, gene, getter):
    try:
        list_files = glob.glob('static/images/imp_plotd*.png')
        for fl in list_files:
            os.remove(fl)
    except:
        None
    if exp != 'Multiome':
        if (getter == False) and (len(gene) > 0):
            new_adata = get_adata_from_exp(exp) 
            fig, ax1 = plt.subplots(1, 1)
            ax1.set_facecolor('floralwhite')
            m = new_adata.obsm['X_spatial']
            if gene == None:
                hold = ax1.scatter(m.T[0], m.T[1], label='_nolegend_', c = 'gray', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 1, vmax = 0.6, vmin = 0)
            else:
                expressions = np.load(os.path.join(r'D:\Alex\MERSCOPE_reanalysis_output\final_figures_avr_only\overall_imputed\imputed', str(gene[0])+'_transfer.npy'))
                replicate_index = np.load(r'C:\Users\amonell\merfish_viewer\website_code\static\detected_transcripts\exp_locations.npy')
                vals = expressions[np.where(replicate_index == new_adata.obs['experiment'][0])]
                hold = ax1.scatter(m.T[0], m.T[1], label='_nolegend_', c = vals, cmap='Greens', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 1, vmax = np.max([0.15, np.percentile(vals, 95)]), vmin = 0)
            
            if exp != '9 hr Avrrpt':
                scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper right', box_color="floralwhite")
            else:
                scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper left', box_color="floralwhite")
            ax1.add_artist(scalebar)
            ax1.grid(False)
            ax1.set_yticks([])
            ax1.set_xticks([])
            ax1.axis('off')
            saverx = os.path.join(app.config['UPLOAD_FOLDER'], 'imp_plotd'+str(time.time()).replace('.', '')+'.png')
            fig.savefig(saverx, dpi = 400, bbox_inches='tight', facecolor='floralwhite')
            plt.close()
        

            fig, ax2 = plt.subplots(1, 1)
            ax2.set_facecolor('floralwhite')
            m = new_adata.obsm['X_spatial']
            if gene == None:
                hold = ax2.scatter(m.T[0], m.T[1], label='_nolegend_', c = 'gray', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 0.2, vmax = 0.6, vmin = 0)
            else:
                try:
                    expressions = np.load(os.path.join(r'D:\Alex\MERSCOPE_reanalysis_output\final_figures_avr_only\atac_heatmap\imputed_atac', str(gene[0])+'_transfer.npy'))
                    replicate_index = np.load(r'C:\Users\amonell\merfish_viewer\website_code\static\detected_transcripts\exp_locations.npy')
                    vals = expressions[np.where(replicate_index == new_adata.obs['experiment'][0])]
                    hold = ax2.scatter(m.T[0], m.T[1], label='_nolegend_', c = vals, cmap='Greens', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 1, vmax = np.max([0.15, np.percentile(vals, 95)]), vmin = 0)
                except:
                    ax2.scatter(m.T[0], m.T[1], label='_nolegend_', color = 'gray', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 0.2, vmax = 0.6, vmin = 0)
                    ax2.set_title('No ATAC Information')
            
            if exp != '9 hr Avrrpt':
                scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper right', box_color="floralwhite")
            else:
                scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper left', box_color="floralwhite")
            ax2.add_artist(scalebar)
            ax2.grid(False)
            ax2.set_yticks([])
            ax2.set_xticks([])
            ax2.axis('off')
            savery = os.path.join(app.config['UPLOAD_FOLDER'], 'imp_plotd'+str(time.time()).replace('.', '')+'.png')
            fig.savefig(savery, dpi = 400, bbox_inches='tight', facecolor='floralwhite')
            plt.close()
            return json.dumps({'saver1': saverx, 'saver2': savery})
        else:
            new_adata = get_adata_from_exp(exp) 
            fig, ax1 = plt.subplots(1, 1)
            ax1.set_facecolor('floralwhite')
            m = new_adata.obsm['X_spatial']
            
            hold = ax1.scatter(m.T[0], m.T[1], label='_nolegend_', color = 'gray', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 0.2, vmax = 0.6, vmin = 0)

            if exp != '9 hr Avrrpt':
                scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper right', box_color="floralwhite")
            else:
                scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper left', box_color="floralwhite")
            ax1.add_artist(scalebar)
            ax1.grid(False)
            ax1.set_yticks([])
            ax1.set_xticks([])
            ax1.axis('off')
            saverx = os.path.join(app.config['UPLOAD_FOLDER'], 'imp_plotd'+str(time.time()).replace('.', '')+'.png').replace('\\', '/')
            fig.savefig(saverx, dpi = 400, bbox_inches='tight', facecolor='floralwhite')
            plt.close()
            if (getter == True) and (gene == None):
                return saverx, saverx
            elif getter == True:
                return json.dumps({'saver1': saverx, 'saver2': saverx})
            else:
                return json.dumps({'saver1': saverx, 'saver2': saverx})
    else:
        if (getter == False) and (len(gene) > 0):
            new_adata = get_adata_from_exp(exp) 
            fig, ax1 = plt.subplots(1, 1)
            ax1.set_facecolor('floralwhite')
            m = new_adata.obsm['X_umap']
            if gene == None:
                hold = ax1.scatter(m.T[0], m.T[1], label='_nolegend_', c = 'gray', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 0.2, vmax = 0.6, vmin = 0)
            else:
                vals = np.array(new_adata[:,np.where(np.array(new_adata.var.index.tolist()) == gene)[0]].X.todense()).T[0]
                hold = ax1.scatter(m.T[0], m.T[1], label='_nolegend_', c = vals, cmap='Greens', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 1, vmax = np.max([0.15, np.percentile(vals, 95)]), vmin = 0)
            
            ax1.grid(False)
            ax1.set_yticks([])
            ax1.set_xticks([])
            ax1.axis('off')
            saverx = os.path.join(app.config['UPLOAD_FOLDER'], 'imp_plotd'+str(time.time()).replace('.', '')+'.png')
            fig.savefig(saverx, dpi = 400, bbox_inches='tight', facecolor='floralwhite')
            plt.close()
        

            savery = saverx
            return json.dumps({'saver1': saverx, 'saver2': savery})
        else:
            new_adata = get_adata_from_exp(exp) 
            fig, ax1 = plt.subplots(1, 1)
            ax1.set_facecolor('floralwhite')
            m = new_adata.obsm['X_umap']
            
            hold = ax1.scatter(m.T[0], m.T[1], label='_nolegend_', c = 'gray', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 1, vmax = 0.6, vmin = 0)

            ax1.grid(False)
            ax1.set_yticks([])
            ax1.set_xticks([])
            ax1.axis('off')
            saverx = os.path.join(app.config['UPLOAD_FOLDER'], 'imp_plotd'+str(time.time()).replace('.', '')+'.png').replace('\\', '/')
            fig.savefig(saverx, dpi = 400, bbox_inches='tight', facecolor='floralwhite')
            plt.close()
            if getter == True:
                return saverx, saverx
            else:
                return json.dumps({'saver1': saverx, 'saver2': saverx})           
def get_ax_pseudo(new_adata, ax1, exp, condition):
    global CURRENT_PSEUDOTIME
    ax1.set_facecolor('floralwhite')
    m = new_adata.obsm['X_spatial']
    if condition == 'raw':
        hold = ax1.scatter(m.T[0], m.T[1], label='_nolegend_', c = new_adata.obs['pseudotime_transfer'].tolist(), cmap='jet', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 1, vmax = 0.6, vmin = 0)
        CURRENT_PSEUDOTIME = 'raw'
    else:
        CURRENT_PSEUDOTIME = 'smoothed'
        hold = ax1.scatter(m.T[0], m.T[1], label='_nolegend_', c = new_adata.obs['smoothed_pseudotime'].tolist(), cmap='jet', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 1, vmax = 0.6, vmin = 0)
    
    if exp != '9 hr Avrrpt':
        scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper right', box_color="floralwhite")
    else:
        scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper left', box_color="floralwhite")
    ax1.add_artist(scalebar)
    ax1.grid(False)
    ax1.set_yticks([])
    ax1.set_xticks([])
    ax1.set_title('MERFISH Spatial Embedding', fontsize = 15, color = 'black') 
    return ax1, hold

def get_ax_rnapseudo(new_adata, ax1):
    ax1.set_facecolor('floralwhite')
    m = new_adata.obsm['X_umap']
    ax1.scatter(m.T[0], m.T[1], label='_nolegend_', c = new_adata.obs['pseudotime'].tolist(), cmap='jet', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 1, vmax = 0.6, vmin = 0)#current_batch.uns['SCT_snn_res.1_transfer_colors'][col]

    ax1.grid(False)
    ax1.set_yticks([])
    ax1.set_xticks([])
    ax1.set_title('Multiome UMAP Embedding', fontsize = 15, color = 'black') 
    return ax1   

def get_ax_merfish(new_adata, ax1, columnars, exp):
    bacteria = columnars.get('bacteria')
    if bacteria == 1:
        bacteria = True
    else:
        bacteria = False

    new_adata.uns['SCT_snn_res.1_transfer_colors'] = ["#91a3b0","#3f5246","#af2b3d","#009088","#94ac78","#721c28","#752f9a","#2aaae1","#418557","#40007f","#7c5914","#9f59f8","#eacd01","#3f3f3f","#ff4c4c", "#ff9f22", "#009088", "#ad3074"]
    ax1.set_facecolor('floralwhite')
    for col in range(len(new_adata.uns['SCT_snn_res.1_transfer_colors'])):
        m = new_adata[new_adata.obs['SCT_snn_res.1_transfer'] == str(col), :].obsm['X_spatial']
        ax1.scatter(m.T[0], m.T[1], label='_nolegend_', color = 'grey', s = 8, marker='.', edgecolors='black', linewidths=0.001, alpha = 0.07)#current_batch.uns['SCT_snn_res.1_transfer_colors'][col]

    for col in range(len(columnars)):
        if (columnars.get(list(columnars.keys())[col]) == 1) and (list(columnars.keys())[col] != 'bacteria'):
            m = new_adata[new_adata.obs['SCT_snn_res.1_transfer'] == str(col), :].obsm['X_spatial']
            ax1.scatter(m.T[0], m.T[1], label='_nolegend_', color = new_adata.uns['SCT_snn_res.1_transfer_colors'][col], s = 14, marker='.', edgecolors='black', linewidths=0.001, alpha = 0.95)
    
    if exp in ['9 hr Avrrpt', '24 hr Avrrpt', '24 hr Kt56']:
        if bacteria == True:
            if exp == '9 hr Avrrpt':
                prefix = '9hr_avr'
            elif exp == '24 hr Avrrpt':
                prefix = '24hr_avr'
            elif exp == '24 hr Kt56':
                prefix = '24hr_kt56'   
            bacteria = np.load(os.path.join('static','detected_transcripts','bacteria_spots', prefix + '.npy'))
            bacteria_adata = sc.AnnData(X = np.zeros((len(bacteria), len(new_adata.var))), var=new_adata.var, obs = ['bacteria'+str(i) for i in range(len(bacteria))])
            bacteria_adata.obs.index = bacteria_adata.obs[0]
            bacteria_adata.obs = pd.read_csv(os.path.join('static','detected_transcripts', 'bacteria_spots', prefix +'_observations.csv'))
            bacteria_adata.obs = bacteria_adata.obs.drop(['Unnamed: 0'], axis=1)
            bacteria_adata.obs['bac_spots'] = bacteria_adata.obs['total_spots_in_colony'] - bacteria_adata.obs['number_hrpl'] - bacteria_adata.obs['number_pvds']
            ax1.scatter(bacteria.T[0], bacteria.T[1], c = bacteria_adata.obs['bac_spots'].tolist(), s = np.array(bacteria_adata.obs['bac_spots'].tolist())*4, cmap = 'cool', linewidths=1, edgecolors='black')
    if exp != '9 hr Avrrpt':
        scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper right', box_color="floralwhite")
    else:
        scalebar = ScaleBar(0.000108, "mm", length_fraction=0.2, font_properties={'size': 8}, location = 'upper left', box_color="floralwhite")
    ax1.add_artist(scalebar)
    ax1.grid(False)
    ax1.set_yticks([])
    ax1.set_xticks([])
    ax1.set_title('MERFISH Spatial Embedding', fontsize = 15, color = 'black') 
    return ax1   

def get_rna_merfish(rna_adata, ax2, columnars):
    matplotlib.rcParams['text.color'] = 'white'
    rna_adata.uns['SCT_snn_res.1_colors'] = ["#91a3b0","#3f5246","#af2b3d","#009088","#94ac78","#721c28","#752f9a","#2aaae1","#418557","#40007f","#7c5914","#9f59f8","#eacd01","#3f3f3f","#ff4c4c", "#ff9f22", "#009088", "#ad3074"]
    ax2.set_facecolor('floralwhite')
    for col in range(len(rna_adata.uns['SCT_snn_res.1_colors'])):
        m = rna_adata[rna_adata.obs['SCT_snn_res.1'] == str(col), :].obsm['X_umap']
        ax2.scatter(m.T[0], m.T[1], label='_nolegend_', color = 'grey', s = 14, marker='.', edgecolors='black', linewidths=0.001, alpha = 0.07)#current_batch.uns['SCT_snn_res.1_transfer_colors'][col]
    for col in range(len(columnars)):
        if columnars.get(list(columnars.keys())[col]) == 1:
            m = rna_adata[rna_adata.obs['SCT_snn_res.1'] == str(col), :].obsm['X_umap']
            ax2.scatter(m.T[0], m.T[1], label='_nolegend_', color = rna_adata.uns['SCT_snn_res.1_colors'][col], s = 14, marker='.', edgecolors='black', linewidths=0.001)
            text = ax2.annotate(str(col), (np.median(m.T[0]), np.median(m.T[1])), fontsize = 10, weight = "bold")
            text.set_path_effects([path_effects.Stroke(linewidth=1, foreground='black'),
                       path_effects.Normal()])
    ax2.grid(False)
    ax2.set_yticks([])
    ax2.set_xticks([])
    ax2.set_title('Multiome UMAP', fontsize = 15, color = 'black')
    return ax2




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)