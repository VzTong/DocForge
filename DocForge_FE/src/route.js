import { createWebHistory } from "vue-router";
import { createRouter } from "vue-router";

const routes = [
    {
        path: "/",
        name: "home",
        component: () => import("./pages/client/Home.vue"),
    },
    // Giữ /convert cho link cũ / đã chia sẻ, tự chuyển sang công cụ mặc định
    {
        path: "/convert",
        redirect: "/convert/md-to-pdf",
    },
    {
        path: "/convert/md-to-pdf",
        name: "convert.md-to-pdf",
        component: () => import("./pages/client/Mdtopdf.vue"),
    },
    {
        path: "/convert/pdf-to-docx",
        name: "convert.pdf-to-docx",
        component: () => import("./pages/client/PdftodocxPage.vue"),
    },
    // Còn lại: Word -> PDF (sắp làm), Audio -> Text, Video -> Text, Dịch
    // transcript bằng AI — thêm route khi từng cái được xây dựng, theo
    // khuôn 2 route phía trên (1 page riêng + 1 composable riêng trong
    // useApi.js theo khuôn useMdToPdfConverter() / usePdfToDocxConverter()).
    {
        path: "/convert/audio-to-text",
        name: "convert.audio-to-text",
        component: () => import("./pages/client/TranscriptEditorPage.vue"),
    },
    // {
    //     path: "/convert/word-to-pdf",
    //     name: "convert.word-to-pdf",
    //     component: () => import("./pages/client/WordToPdfPage.vue"),
    // },
    // {
    //     path: "/convert/video-to-text",
    //     name: "convert.video-to-text",
    //     component: () => import("./pages/client/VideoToTextPage.vue"),
    // },
    // {
    //     path: "/convert/translate-transcript",
    //     name: "convert.translate-transcript",
    //     component: () => import("./pages/client/TranslateTranscriptPage.vue"),
    // },

    // {
    //     path: "/car-details/:id",
    //     name: "car.details",
    //     component: () => import("./pages/client/CarDetails.vue"),
    // },
    // {
    //     path: "/car-list",
    //     name: "car.list",
    //     component: () => import("./pages/client/CarList.vue"),
    // }
    // {
    //     path: "/admin/danh-muc",
    //     name: "admin.category",
    //     component: () => import("./pages/admin/product_cate/List.vue"),
    // },
    // {
    //     path: "/admin/danh-muc/them-moi",
    //     name: "admin.category.create",
    //     component: () => import("./pages/admin/product_cate/Create.vue"),
    // },
    // {
    //     path: "/admin/danh-muc/sua/:id",
    //     name: "admin.category.edit",
    //     component: () => import("./pages/admin/product_cate/Edit.vue"),
    // },
    // {
    //     path: "/admin/san-pham/them-moi",
    //     name: "admin.product.create",
    //     component: () => import("./pages/admin/product/Create.vue")
    // },
    // {
    //     path: "/admin/san-pham",
    //     name: "admin.product.list",
    //     component: () => import("./pages/admin/product/List.vue")
    // },
    // {
    //     path: "/admin/san-pham/sua/:id",
    //     name: "admin.product.edit",
    //     component: () => import("./pages/admin/product/Edit.vue"),
    // },
    // {
    //     path: "/admin/danh-sach-don-hang",
    //     name: "admin.orders",
    //     component: () => import("./pages/admin/order/orders.vue")
    // },
    // {
    //     path: "/dang-ky",
    //     name: "register",
    //     component: () => import("./pages/account/Register.vue")
    // },
    // {
    //     path: "/dang-nhap",
    //     name: "login",
    //     component: () => import("./pages/account/Login.vue")
    // }
    // {
    //     path: "/gio-hang",
    //     name: "cart",
    //     component: () => import("./pages/client/Cart.vue")
    // },
    // {
    //     path: "/dat-hang",
    //     name: "checkout",
    //     component: () => import("./pages/client/Checkout.vue")
    // }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;