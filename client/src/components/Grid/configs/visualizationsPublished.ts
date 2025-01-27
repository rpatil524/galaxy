import { fetcher } from "@/api/schema";
import Filtering, { contains, expandNameTag, type ValidFilter } from "@/utils/filtering";
import { withPrefix } from "@/utils/redirect";

/**
 * Api endpoint handlers
 */
const getVisualizations = fetcher.path("/api/visualizations").method("get").create();

/**
 * Local types
 */
type SortKeyLiteral = "create_time" | "title" | "update_time" | "username" | undefined;
type VisualizationEntry = Record<string, unknown>;

/**
 * Request and return data from server
 */
async function getData(offset: number, limit: number, search: string, sort_by: string, sort_desc: boolean) {
    const { data, headers } = await getVisualizations({
        limit,
        offset,
        search,
        sort_by: sort_by as SortKeyLiteral,
        sort_desc,
        show_own: false,
        show_published: true,
        show_shared: true,
    });
    const totalMatches = parseInt(headers.get("total_matches") ?? "0");
    return [data, totalMatches];
}

/**
 * Declare columns to be displayed
 */
const fields = [
    {
        title: "Title",
        key: "title",
        type: "link",
        width: "30%",
        handler: (data: VisualizationEntry) => {
            window.location.href = withPrefix(`/plugins/visualizations/${data.type}/saved?id=${data.id}`);
        },
    },
    {
        key: "annotation",
        title: "Annotation",
        type: "text",
    },
    {
        key: "username",
        title: "Owner",
        type: "text",
    },
    {
        key: "tags",
        title: "Tags",
        type: "tags",
        disabled: true,
    },
    {
        key: "update_time",
        title: "Updated",
        type: "date",
    },
];

/**
 * Declare filter options
 */
const validFilters: Record<string, ValidFilter<string | boolean | undefined>> = {
    title: { placeholder: "title", type: String, handler: contains("title"), menuItem: true },
    slug: { handler: contains("slug"), menuItem: false },
    tag: {
        placeholder: "tag(s)",
        type: "MultiTags",
        handler: contains("tag", "tag", expandNameTag),
        menuItem: true,
    },
};

/**
 * Grid configuration
 */
export default {
    fields: fields,
    filtering: new Filtering(validFilters, undefined, false, false),
    getData: getData,
    plural: "Visualizations",
    sortBy: "update_time",
    sortDesc: true,
    sortKeys: ["create_time", "title", "update_time"],
    title: "Published Visualizations",
};
